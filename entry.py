from allmyfunctions import *

# search for strings in the file 'sample.txt'
# will loop infinitely
# replace the list of items with a proper array of strings, to recieve via mqtt or rest idk yet
# storagedump()
# newEntry()
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
