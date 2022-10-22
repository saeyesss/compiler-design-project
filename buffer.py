def load_buffer():
    buffer = []
    cont = 1

    openFile = open('prog.c', 'r')
    text = openFile.readline()

    while text != "":
        buffer.append(text)
        text = openFile.readline()
        cont += 1

        if cont == 10 or text == "":
            # return the full buffer
            buf = "".join(buffer)
            cont = 1
            yield buf
            # reset buffer
            buffer = []

    openFile.close()


