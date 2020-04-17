from mainInterface import MainInterface
import asyncio, nest_asyncio
nest_asyncio.apply()

def main(async_loop):
    interface = MainInterface(async_loop)
    interface.mainloop()
    
if __name__=="__main__":
    async_loop = asyncio.get_event_loop()
    main(async_loop)
