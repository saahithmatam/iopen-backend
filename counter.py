para = 'DMA, Direct Memory Access, is an improvement over interrupt-driven I/O, because by the time an interrupt notifies the processor of completion, the DMA module has already moved or executed the data. It utilizes the usage of cache in order to retrieve data faster and more efficiently.'
count = 0

for i in para:
    if i==".":
        count = count + 1


print("This is the number of sentences: ", count)
        
