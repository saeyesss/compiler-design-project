def load_buffer():
    buffer = []
    cont = 1

    openfile = open('test_program.c', 'r')
    text = openfile.readline()

    while text != "":
        buffer.append(text)
        text = openfile.readline()
        cont += 1

        if cont == 10 or text == "":
            # return the full buffer
            buf = "".join(buffer)
            cont = 1
            yield buf
            # reset buffer
            buffer = []

    openfile.close()


