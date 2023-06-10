import os
import sys
import argparse
import concurrent.futures
from . import run

INIT_SUCCESS = 6

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='subparser')

    debug_sub_parser = subparser.add_parser('eosdebugger', help='start eos debugger server')
    debug_sub_parser.add_argument('--addr', default="127.0.0.1", help="eos debugger server address, default to 127.0.0.1")
    debug_sub_parser.add_argument('--server-port', default="9090", help="eos debugger server port, default to 9090")
    debug_sub_parser.add_argument('--vm-api-port', default="9092", help="eos debugger vm api port, default to 9092")
    debug_sub_parser.add_argument('--rpc-server-port', default="9093", help="rpc server port, default to 9093")
    debug_sub_parser.add_argument('--apply-request-addr', default="127.0.0.1", help="client side apply request server address, default to 127.0.0.1")
    debug_sub_parser.add_argument('--apply-request-port', default="9091", help="client side apply request server port, default to 9091")

    start_eos_parser = subparser.add_parser('eosnode', help='run a eos node')

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(-1)

    if 'RUN_IPYEOS' in os.environ:
        import time
        import asyncio
        import signal
        from ipyeos import eos
        from ipyeos import server
        from aiohttp import web

        async def quit_app(request):
            eos.post(eos.quit)
            return web.Response(text="Done!\n"+ str(time.time()))

        async def hello(request):
            def say_hello(name):
                print('hello', name)
                return name
            outputs = []
            for i in range(10):
                start = time.time()
                ret = eos.post(say_hello, 'alice')
                end = time.time()
                outputs.append(f"post test: {ret} diff: {int((end - start)*1e6)}")
            return web.Response(text='\n'.join(outputs))

        async def start_webserver():
            app = web.Application()
            app.router.add_get('/quit', quit_app)
            app.router.add_get('/', hello)
            runner = web.AppRunner(app)
            await runner.setup()
            try:
                site = web.TCPSite(runner, 'localhost', 7777)
            except Exception as e:
                print(e)
                site = web.TCPSite(runner, 'localhost', 7778)
            await site.start()
            print('++++++++++++server started!!')
            while True:
                await asyncio.sleep(3600) # serve forever

        if sys.argv[1] == 'eosnode':
            def run_eos():
                argv = sys.argv[1:]
                argv[0] = 'ipyeos'
                ret = eos.init(argv)
                if not ret == 0:
                    print('init return', ret)
                    return
                ret = eos.run()
                # while True:
                #     ret = eos.run_once()
                #     if not ret == 0:
                #         break
                #     await asyncio.sleep(0.0)
                #     print('run once')
                print('run return', ret)

            async def main():
                asyncio.create_task(start_webserver())
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
                future = asyncio.get_event_loop().run_in_executor(executor, run_eos)
                result = await future
                print("Result: ", result)
            asyncio.run(main())
        elif sys.argv[1] == 'eosdebugger':
            result, unknown = parser.parse_known_args()
            server.start_debug_server(result.addr, result.server_port, result.vm_api_port, result.apply_request_addr, result.apply_request_port, result.addr,result.rpc_server_port)                
        else:
            parser.print_help()
    else:
        if sys.argv[1] in ['eosnode', 'eosdebugger']:
            custom_cmds = ['-m', 'ipyeos']
            custom_cmds.extend(sys.argv[1:])
            run.run_ipyeos(custom_cmds)
        else:
            run.run_ipyeos()

if __name__ == "__main__":
    main()
