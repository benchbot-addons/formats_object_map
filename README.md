# BenchBot Add-on: Format definition for "object maps"

This add-on includes the format definition for an "object map". Specification
for two variations are also included:

- "raw": used for specifying ground truth object maps
- "state": each object also specifies a state (e.g. added / removed when used in scene change detection)

## Format Details
### `object_map_ground_truth`
The `object_map_ground_truth` is the ground-truth format for object maps defined by a list of semantic axis-aligned 3D cuboids:
- An object's semantic label is provided by a `class` name (string) and a class `id` (integer).
- An object's cuboid spatial geometry is defined by describing the location (`'centroid'`) of an axis-aligned cuboid in 3D space, whose dimensions are `'extent'`.

The format of an `object_map_ground_truth` is outlined below:
```
{
  'objects': [
    {
      'class': <class_name>,
      'id': <class_id>
      'centroid': [<xc>, <yc>, <zc>],
      'extent': [<xe>, <ye>, <ze>],
    },
    ...
  ]
  'class_list': [<classes_order>]
  'synonyms': {
    <synonym>:<class_name>,
    ...
  }
}
```

- For each object in the objects list`'objects'`:
  - `class` is the class name of an object given as a string
  - `id` is the class id number of an object given as an integer.
    - **Note** that class `id` is specific to a given class list and should not be defined unless a class list is provided and may change depending on class list during evaluation.
  - `'centroid'` is the 3D coordinates for the centre of the object's cuboid (must be a list of 3 numbers)
  - `'extent'` is the **full** width, height, & depth of the cuboid (must be a list of 3 numbers)
    - **Note** the cuboid described by `'centroid'` & `'extent'` must be axis-aligned in global coordinates, & current units in supplied environments are metres
- `class_list` supplies the list of classes that could be examined as part of an experiment using this ground truth
  - **Note** this can include classes outside of the ones actually present in the given environment map.
  - If a `class_list` is not provided, one will currently be extracted from an environment's `object_list` if available.
- `synonyms` supplies a set of synonyms that are acceptable for any given class name in corresponding results object maps.
  - This is optional to give researchers flexibility when defining their own class lists as they develop their own results

### `object_map`
The `object_map` format is our results format defines a proposed object-based semantic map as a list of objects with information about both their semantic label & spatial geometry:
- Semantic label information is provided through a probability distribution (`'label_probs'`) across either a provided (`'class_list'`), or our a default class list defined during evaluation by the ground_truth class list
  - **WARNING** depending on the default class list can be extremely risky. Always ensure that your class list corresponds with the output you are providing and matches classes you are evaluating against. Synonyms can be used but only if they match those provided with ground truth.
- Spatial geometry information is provided in the same manner as the `object_map_ground_truth` format above by defining the `centroid` and `extent` of axis-aligned 3D cuboids.

The results format as it will look when submitted for evaluation is outlined below:
```
{
    'task_details': <task_details>,
    'environment_details': <environment_details>,
    'results: {
      'objects': [
          {
              'label_probs': [<object_class_probability_distribution>],
              'centroid': [<xc>, <yc>, <zc>],
              'extent': [<xe>, <ye>, <ze>],
          },
          ...
      ]
      'class_list': [<classes_order>]
    }
}
```

**Note** that `<task_details>` and `<environment_details>` should already be provided by the benchbot system for the given task and environment. Users should only need to input data for `objects` and `class_list`.

- For each object in `'objects'` the objects list:
  - `'label_probs'` is the probability distribution for the suggested object label corresponding to the class list in `'class_list'`, or our default class list above (must be a list of numbers)
  - `'centroid'` is the 3D coordinates for the centre of the object's cuboid (must be a list of 3 numbers)
  - `'extent'` is the **full** width, height, & depth of the cuboid (must be a list of 3 numbers)
    - **Note** the cuboid described by `'centroid'` & `'extent'` must be axis-aligned in global coordinates, & current units in supplied environments are metres
  - `'class_list'` is a list of strings defining a custom order for the probabilities in the `'label_probs'` distribution field of objects (if not provided the default class list & order is assumed).
    - there is some support given for class name synonyms depending on evaluaiton measure (supported by [OMQ](https://github.com/benchbot-addons/eval_omq)).
    - While `class_list` is technically optional, it is *highly recommended* that all results submitted should include it to ensure no confusion upon evaluation.

### `object_map_with_states`
The `object_map_with_states` format is our results format that defines a proposed object-based semantic map wherein objects may have been added or removed from a scene.

This format is identical to the format shown in [`object_map`](#object_map), however each object now has the following format:

```
{
  'label_probs': [<object_class_probability_distribution>],
  'centroid': [<xc>, <yc>, <zc>],
  'extent': [<xe>, <ye>, <ze>],
  'state_probs': [<pa>, <pr>, <pu>]
}
```
where `<pa>`, `<pr>`, and `<pu>` are the probabilities given that the object has been added, removed, and remains unchanged respectively.

**Note** if your system is not probabilistic, simply use all 0s & a single 1 for any of the distributions above (e.g. `'state_probs'` of  `[1, 0, 0]` for an added object)