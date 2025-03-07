from pathlib import Path
from json import load
from mothpriest.references import IDListReference, IDReference
from mothpriest.parsers import *
from ..tools.decompress import decompress
from ..parsers import parse_ess

def readMapping(input_file: Path):
    """Reads a mapping file and returns its content"""

    if not input_file.exists():
        raise FileNotFoundError(f'Could not find mapping file {input_file}')
    with open(input_file, 'r') as f:
        content = load(f)
    return content

def getLoadOrder(ess_parser: BlockParser):
    """Retrieve the load order from a save record"""
    plugin_wstrings = ess_parser.getReference([
        'mainContent',
        'compressedContainer',
        'pluginInfo',
        'pluginInfoEntries'
    ])
    return plugin_wstrings.mapReference('value', True)

def getFormIDs(ess_parser):
    """Retrieve the FormIDs from a save record (both the formIDArray and visitedWorldspaceArray)"""

    array_reference = IDListReference([
        'mainContent',
        'compressedContainer',
        'formIDArray'
    ])

    formID_array = array_reference.retrieveRecord(ess_parser)

    visited_worldspace_reference = IDListReference([
        'mainContent',
        'compressedContainer',
        'visitedWorldspaceArray'
    ])

    visited_worldspace_array = visited_worldspace_reference.retrieveRecord(ess_record)

    return formID_array, visited_worldspace_array

def patchSaveMerge(
    input_file: Path, 
    map_file: Path, 
    merge_name: str, 
    output_file: Path
):
    """Patches a Skyrim save using a map file from a plugin merge"""

    # read mapping from merge
    mapping = readMapping(map_file)
    plugin_names = list(mapping.keys())

    print(f"preparing to rewrite save to reflect merge of plugins {plugin_names} into merged plugin {merge_name}")

    # parse and decompress ess save file
    parser = parse_ess(input_file)
    print("save file parsed successfully...")

    # get the current plugin load order from the save file
    plugin_info: ReferenceCountParser = parser.getReference(['mainContent', 'compressedContainer', 'compressedData', 'main_content', 'pluginInfo', 'pluginInfoEntries'])
    load_order = plugin_info.mapReference('value', True)

    print(f"found original load order: {load_order}...")

    # find merged plugin ids
    plugin_ids = {}
    for plugin_name in plugin_names:
        try:
            plugin_ids[plugin_name] = load_order.index(plugin_name)
        except ValueError:
            print(f'{plugin_name} not found in save file, skipping')

    # print(plugin_ids)

    # Assumes that the new merged plugin will occupy the earliest
    #   of all of its merge plugin slots
    combined_id = plugin_ids[min(plugin_ids, key=plugin_ids.get)]
    
    print(f'replacing plugin {load_order[combined_id]} with merged plugin {merge_name}...')
    plugin_info[combined_id, 'value'] = merge_name
    for id in plugin_ids.values():
        if id > combined_id:
            print(f'removing plugin {plugin_info[id, "value"]} from load order...')
            del plugin_info[id]


    # determine new load order
    merged_ids = set(plugin_ids.values())
    new_load_order = load_order[:combined_id]
    order_map_list = list(range(0, combined_id+1))
    new_load_order.append(merge_name)
    for i in range(combined_id+1, len(load_order)):
        if i not in plugin_ids.values():
            new_load_order.append(load_order[i])
            order_map_list.append(max(order_map_list)+1)
        else:
            order_map_list.append(combined_id)

    print(f"setting new load order: {new_load_order}...")

    for t, p in zip(plugin_info.mapReference('value', True), new_load_order):
        assert p == t, f'{p} != {t}'


    # get FormIDs
    formID_array = parser['mainContent', 'compressedContainer', 'compressedData', 'main_content', 'formIDArray']
    visitedWorldspace_array = parser['mainContent', 'compressedContainer', 'compressedData', 'main_content', 'visitedWorldspaceArray']

    id_to_map = {plugin_ids[name] : m for (name, m) in mapping.items()}

    # iterate and map
    # TODO this assumes that the first plugin in a merge will need no renumbering
    for i in range(0, len(formID_array)):
        formID = formID_array[i]
        pluginID = formID['pluginID']
        #TODO make this variable behavior (not all saves may use 254 for esl plugins)
        if pluginID == 254:
            continue
        new_pluginID = order_map_list[pluginID]
        objectID = formID['objectID']
        if pluginID in merged_ids:
            object_map = id_to_map[pluginID]
            if objectID in object_map:
                new_objectID = object_map[objectID]
                formID_array[i]['objectID'] = new_objectID
                print(f'mapping for plugin with old ID {pluginID}: {objectID} -> {new_objectID}...')

        if pluginID == new_pluginID:
            continue
        formID_array[i]['pluginID'] = new_pluginID
        print(f'mapping plugin ID {pluginID} -> {new_pluginID}...')

    for i in range(0, len(visitedWorldspace_array)):
        formID = visitedWorldspace_array[i]
        pluginID = formID['pluginID']
        new_pluginID = order_map_list[pluginID]
        objectID = formID['objectID']
        if pluginID in merged_ids:
            object_map = id_to_map[pluginID]
            if objectID in object_map:
                new_objectID = object_map[objectID]
                visitedWorldspace_array[i]['objectID'] = new_objectID
                print(f'mapping for plugin worldspace object with old ID {pluginID}: {objectID} -> {new_objectID}...')

    with BytesIO() as outBuffer:
        parser.unparse(outBuffer)
        outBuffer.seek(0)
        outBytes = outBuffer.read()

    with open(output_file, 'wb') as f:
        f.write(outBytes)

    print(f"All operations complete, history has been rewritten. Make sure your load order matches the new load order above!")