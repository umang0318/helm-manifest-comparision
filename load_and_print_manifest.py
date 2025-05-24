#https://learningactors.com/python-yaml-and-kubernetes-the-art-of-mastering-configuration/
import yaml
import pprint
import json

def print_manifest(manifest_data):
    for data in manifest_data:
        pprint.pprint(data)

def load_and_print_manifest(filename):
    with open(filename, 'r') as f:
        all_data = yaml.safe_load_all(f.read())
    return all_data

def get_kubernetes_objects(manifest_data):
    kubernetes_objects = {}
    for data in manifest_data:
        #print(yaml.dump(data, default_flow_style=False))
        key = (data['kind'], data['metadata']['name'])
        kubernetes_objects[key] = data
    return kubernetes_objects

# def compare_manifests(manifests1, manifests2):
#     keys1 = set(manifests1.keys())
#     keys2 = set(manifests2.keys())
#
#     added = keys2 - keys1
#     removed = keys1 - keys2
#     common = keys1 & keys2
#
#     modified = []
#     for key in common:
#         yaml1 = yaml.dump(manifests1[key], sort_keys=True)
#         yaml2 = yaml.dump(manifests2[key], sort_keys=True)
#         if yaml1 != yaml2:
#             modified.append((key, yaml1, yaml2))
#
#     return added, removed, modified

def flatten_json(data, parent_key='', sep='.'):
    items = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten_json(v, new_key, sep=sep))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_key = f"{parent_key}[{i}]"
            items.update(flatten_json(v, new_key, sep=sep))
    else:
        items[parent_key] = data
    return items

def flat_object_dict(keys,kubernetes_objects):
    flat_objects = {}
    for key in keys:
        resource = kubernetes_objects[key]
        #print(resource_existing)
        if resource:
            object_name = list(key)
            object_name = "-".join(key)

            flat_objects[object_name] = flatten_json(resource)
        # for key, value in resource.items():
        #     print(f"{key}: {value}")

    print("Flattened  existing objects:")
    print(json.dumps(flat_objects, indent=2))  # Pretty print

    return flat_objects

def compare_kubernetes_objects(kubernetes_object1, kubernetes_object2):
    pass

def main():
    example_file1 = 'helm-manifest1.yaml'
    example_file2 = 'helm-manifest2.yaml'

    file1 = load_and_print_manifest(example_file1)
    file2 = load_and_print_manifest(example_file2)

    #print_manifest(file1)
    #print_manifest(file2)


    kubernetes_objects_existing = get_kubernetes_objects(file1)
    #print(kubernetes_objects_existing)

    #print("******")

    kubernetes_objects_new = get_kubernetes_objects(file2)
    #print(kubernetes_objects_new)

    #print("#####")

    keys_existing = set(kubernetes_objects_new.keys())
    #print(keys_existing)

    #print("$$$$$$")
    keys_new = set(kubernetes_objects_new.keys())
    #print(keys_new)

    #print("%%%%%%%%%")

    #for key in keys_existing:
        #value_existing = kubernetes_objects_existing[key]
        #print(value_existing)

    #add, rm, mod = compare_manifests(kubernetes_objects_existing, kubernetes_objects_new)
    #print("%%%%%%%%%")
    #print(add)
    #print("^^^^^^^^^")
    #print(rm)
    #print("$$$$$$$$$$$")
    #print(mod)

    existing_manifest_flat_dict = flat_object_dict(keys_existing, kubernetes_objects_existing)
    new_manifest_flat_dict = flat_object_dict(keys_new, kubernetes_objects_new)

    print("Existing manifest:")
    pprint.pprint(existing_manifest_flat_dict, indent=2)

    print("New manifest:")
    pprint.pprint(new_manifest_flat_dict, indent=2)





if __name__ == '__main__':
    main()