from os import listdir
#from PIL import Image
import os, os.path
import tensorflow as tf, sys
from multiprocessing import Pool

patharg = sys.argv[1]
#path = "E:/project/test/output/"
valid_images = [".jpg",".gif",".png",".jpeg"]

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
    in tf.gfile.GFile("output_labels.txt")]
# Unpersists graph from file
with tf.gfile.GFile("output_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def score_warn(a):
            categ = label_lines[a]
            if categ == 'road' or categ == 'sky':
                print('\nSAFE TO MOVE')
            else:
                print('\nWARNING TO USER')


def test_image(image_det):
    # Read in the image_data
    image_data = tf.gfile.GFile(image_det[0], 'rb').read()
    
    # Feed the image_data as input to the graph and get first prediction
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, 
         {'DecodeJpeg/contents:0': image_data})        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        print('\n TEST RESULTS :  ' + str(image_det[1]) + '\n')
        lst = top_k[0]
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
        score_warn(lst)

def loadImages(path):
    # return array of images
    imagesList = listdir(path)
    list_of_images = []
    processes = []
    img_name = []
    #loadedImages = []
    for image in imagesList:
        ext = os.path.splitext(image)[1]
        if ext.lower() not in valid_images:
               continue
        img = (os.path.join(path,image))
        #img = Image.open(os.path.join(path,image))
        #loadedImages.append(img)
        list_of_images.append(img)
        img_name.append(image)
    return list_of_images,img_name
    # for imgs in zip(list_of_images,img_name):
    #     p = Process(target=test_image, args=(imgs[0],imgs[1]))
    #     p.start()
    #     processes.append(p)
    # for proc in processes:
    #     proc.join()

def main():
    return loadImages(patharg)

if __name__ == "__main__": 
    l,n = main()
    m=[]
    x = zip(l,n)
    for i in x:
        print(i)
        m.append(i)
    with Pool(5) as p:
        p.map(test_image, m)



