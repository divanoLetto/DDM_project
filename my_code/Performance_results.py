import cv2
import matplotlib.pyplot as plt

from my_code.settings import CLUSTERED_PATH


def plot_barcode_histrogramm(all_barcodes):
    fig = plt.figure()
    print("Plotting histogramm")
    axes = plt.axes()
    size = len(all_barcodes.keys())
    axes.set_xticks(range(0, size), int(size / 20))
    y = all_barcodes.values()
    x = range(0, len(y))
    plt.bar(x, y, color='g')
    plt.show()


def draw_assigmente_bfp_outcome(list_bfp, image_name, df, specify_name = "" ):
    image_path = CLUSTERED_PATH + image_name
    image = cv2.imread(image_path)
    image = image.copy()
    for bfp in list_bfp:
        if bfp.get_cluster() is not None:
            center = bfp.get_cluster().calc_cluster_center()
            center = [int(center[0]) -100, int(center[1])]
            image = cv2.putText(image, text=str(bfp.get_barcode()), org=tuple(center), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2.5, color=(193, 160, 255), thickness=9)
            center2 = [int(center[0]) -100, int(center[1])-100]
            collocation = (df.loc[df['barcode'] == bfp.get_barcode()])["collocation"].values[0]
            image = cv2.putText(image, text=str(collocation), org=tuple(center2), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2.5, color=(193, 90, 255), thickness=9)
    cv2.imwrite(CLUSTERED_PATH + specify_name + image_name, image)


def draw_word_in_cluster(image_name, cluster, word, offset_x=0, offset_y=0, color = (0,0,255)):
    image_path = CLUSTERED_PATH + image_name
    image = cv2.imread(image_path)
    center = cluster.calc_cluster_center()
    center = [int(center[0] + offset_x), int(center[1] + offset_y)]
    image = cv2.putText(image, text=str(word), org=tuple(center), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2.5, color=color, thickness=9)
    cv2.imwrite(CLUSTERED_PATH + image_name, image)

