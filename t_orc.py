from service.TextProcessor import TextProcessor


def main():
    text = "值越T,会使输出更随机，更具创造性\n；值越1，输出会更加稳定或确定"
    processor = TextProcessor('input', text)
    processor.action('ai')


if __name__ == '__main__':
    main()
