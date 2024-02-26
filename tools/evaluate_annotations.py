import json

PATH = '/home/st/Documents/Uni/Masterarbeit/Data/2024-02-26_rows.json'

if __name__ == '__main__':
    rows = json.load(open(PATH, 'r'))
    total_annotations = 0
    total_annotations_de = 0
    total_annotations_en = 0
    double_annotations = 0
    double_annotations_de = 0
    double_annotations_en = 0
    total_complete_agreement = 0
    one_sided = 0
    overlap = 0
    no_agreement = 0
    no_agreement_answer = 0

    total_spans = 0
    total_selected = 0
    total_selected_double = 0
    total_agreed = 0
    total_agreed_selected = 0
    total_disagreed_selected = 0

    for row in rows:
        # Exclude title
        current_spans = len(row['context'].split('\n')) - 1

        for question in row['questions']:
            annotations = [question for question in question['annotations'] if not question['skipped'] and not question['archived']]
            annotations_length = len(annotations)
            total_annotations += annotations_length

            if row['language'] == 'de':
                total_annotations_de += annotations_length
            elif row['language'] == 'en':
                total_annotations_en += annotations_length

            if annotations_length == 2:
                annotation_0 = annotations[0]['answerLines']
                annotation_1 = annotations[1]['answerLines']

                # if len(annotation_0) > 4 or len(annotation_1) > 4:
                #     continue

                double_annotations += 1
                if row['language'] == 'de':
                    double_annotations_de += 1
                elif row['language'] == 'en':
                    double_annotations_en += 1

                diff_0 = list(set(annotation_0).difference(annotation_1))
                diff_1 = list(set(annotation_1).difference(annotation_0))

                if len(diff_0) == 0 and len(diff_1) == 0:
                    total_complete_agreement += 1
                elif (len(diff_0) == 0 or len(diff_1) == 0) and not len(annotation_0) == 0 and not len(annotation_1) == 0:
                    one_sided += 1
                elif len(list(set(annotation_0).intersection(annotation_0))) > 0:
                    overlap += 1
                else:
                    if (len(annotation_0) == 0) != (len(annotation_1) == 0):
                        no_agreement_answer += 1
                    no_agreement += 1

                if len(diff_0) != 0 and len(diff_1) != 0:
                    print(sorted(annotation_0))
                    print(sorted(annotation_1))
                    print('\n')

                total_agreed += current_spans - len(diff_0) - len(diff_1)
                total_agreed_selected += len(annotation_0) - len(diff_0)
                total_disagreed_selected += len(diff_0) + len(diff_1)

                total_spans += current_spans
                total_selected += (len(annotation_0) + len(annotation_1)) / 2

            for annotation in annotations:
                if annotation['comment'] != "":
                    print(annotation['comment'], annotation['user'])

    print('total annotations:', total_annotations)
    print('total annotations de:', total_annotations_de)
    print('total annotations en:', total_annotations_en)
    print('double annotations:', double_annotations)
    print('double annotations de:', double_annotations_de)
    print('double annotations en:', double_annotations_en)
    print('complete agreement:', total_complete_agreement, ' | ', total_complete_agreement/double_annotations, 2)
    print('one sided:', one_sided, ' | ', one_sided/double_annotations, 2)
    print('overlap:', overlap, ' | ', overlap/double_annotations, 2)
    print('no agreement:', no_agreement, ' | ', no_agreement/double_annotations, 2)
    print('no agreement answer:', no_agreement_answer, ' | ', no_agreement_answer / double_annotations, 2)
    #
    # print('total span:', total_spans)
    # print('total selected:', total_selected)
    # print('total agreed:', total_agreed)
    # print('total agreed selected:', total_agreed_selected)
    # print('total disagreed selected:', total_disagreed_selected)
