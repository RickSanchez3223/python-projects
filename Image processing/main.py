import os
import cv2


class ImageHandler:
    def __init__(self):
        self.image = None
        self.image_name = None

    @staticmethod
    def calculate_new_dim(scale_percent, width, height):
        width *= scale_percent / 100
        height *= scale_percent / 100
        return int(width), int(height)

    def read_image(self, path=None):
        self.image = cv2.imread(path)
        self.image_name = path.split('/')[-1]

    def resize_image_to_scale(self, scale_percent):
        if self.image is not None:
            new_dim = self.calculate_new_dim(scale_percent, self.image.shape[1], self.image.shape[0])
            resized_image = cv2.resize(self.image, new_dim)
            return resized_image

        else:
            raise Exception('No image to be processed.')

    def resize_image(self, output_directory):
        # Below are the image resolution sets required
        new_dims = [[150, 150], [800, 600]]
        for new_dim in new_dims:
            new_image_path = f"{output_directory}/{new_dim[0]}_{new_dim[1]}_{self.image_name}"
            resized_image = cv2.resize(self.image, new_dim)
            self.save(resized_image, path=new_image_path)

    @staticmethod
    def save(image_obj, path):
        cv2.imwrite(path, image_obj)


def resize_images(input_directory, output_directory):
    # Resizes all images in input_directory to a output_directory
    image = ImageHandler()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    source_images = os.listdir(input_directory)
    for source_image in source_images:
        source_image_path = f"{input_directory}/{source_image}"
        image.read_image(path=source_image_path)
        image.resize_image(output_directory=output_directory)

        # resized_image = image.resize_image_to_scale(scale_percent=50)
        # image.save(resized_image, path=f"{output_directory}/50_{source_image}")
        # resized_image = image.resize_image_to_scale(scale_percent=50)
        # image.save(resized_image, path=f"{output_directory}/50_{source_image}")
    print('completed')


if __name__ == '__main__':
    resize_images(input_directory='source-images', output_directory='resized')
