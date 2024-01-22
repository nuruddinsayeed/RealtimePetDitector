import os
from glob import glob
from bs4 import BeautifulSoup
from pathlib import Path


def get_sorted_annotations(dir_path: str) -> list:
    return list(sorted(glob(f'{dir_path}/*.xml')))


def create_labels(annotation_path: str):
    sorted_xml_paths = get_sorted_annotations(annotation_path)
    print(f'sorted paths: \n{sorted_xml_paths[:5]}')
    
    labels_destination = f'{annotation_path}/labels'
    os.makedirs(labels_destination, exist_ok=True)

    for xml_path in sorted_xml_paths:
        with open(xml_path, 'r') as f:
            data = f.read()
            soup = BeautifulSoup(data, 'xml')

            image_size = soup.find('size')
            img_width = int(image_size.find('width').text)
            img_height = int(image_size.find('height').text)

            objects = soup.find_all('object')
            obj_list = list()
            class_labda = lambda x: 0 if x == 'cat' else 1

            for obj in objects:
                label = class_labda(obj.find('name').text)

                xmin = int(obj.find('xmin').text)
                ymin = int(obj.find('ymin').text)
                xmax = int(obj.find('xmax').text)
                ymax = int(obj.find('ymax').text)

                x = ((xmin + xmax) / 2) / img_width
                y = ((ymin + ymax) / 2) / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height

                obj_list.append([label, x, y, width, height])
        
                
                
            # path_length = len(xml_path)
            # file_name = xml_path[20:path_length - 4]
            file_name = Path(xml_path).stem
        
            txt_label_dir = labels_destination + '/' + file_name + '.txt'
        
            with open(txt_label_dir, 'w', ) as f :
                
                for obj in obj_list :
                                    
                    f.write(str(obj[0]) + ' ' +\
                            str(obj[1]) + ' ' +\
                            str(obj[2]) + ' ' +\
                            str(obj[3]) + ' ' +\
                            str(obj[4]))


if __name__ == '__main__':
    create_labels(annotation_path='vak_xml')
    create_labels(annotation_path='train_xml')

