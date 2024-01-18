from service.OutlineProcessor import OutlineProcessor as Processor


def main():
    processor = Processor('file')
    processor.do()


if __name__ == '__main__':
    main()
