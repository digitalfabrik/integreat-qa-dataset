import json

PATH = '/home/st/Documents/Uni/Masterarbeit/Data/2024_02_13_rows.json'

if __name__ == '__main__':
    rows = json.load(open(PATH, 'r'))
    total_annotations = 0
    double_annotations = 0

    for row in rows:
        for question in row['questions']:
            annotations_length = len(question['annotations'])
            total_annotations += annotations_length
            if annotations_length > 1:
                double_annotations += len(question['annotations'])

            for annotation in question['annotations']:
                if annotation['comment'] != "":
                    print(annotation['comment'], annotation['user'])

    print(total_annotations)
    print(double_annotations)
