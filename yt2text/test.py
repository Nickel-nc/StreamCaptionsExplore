"""
Usage Example
"""

import os
from preprocessor import YT2Text
import json
import gc
import speech_recognition as sr
urls = [
    "https://www.youtube.com/watch?v=z0cWBDUOce4",
    "https://www.youtube.com/watch?v=wyqfYJX23lg",
    "https://www.youtube.com/watch?v=R9U5qEp_7eE",
    "https://www.youtube.com/watch?v=nASEuHbyUB0",
    "https://www.youtube.com/watch?v=xcmJiuK38Yw",
]

if __name__ == "__main__":


    for url in urls:
        print("processing:", url)
        yt = YT2Text()  # assembled wrapper
        result = yt.run(url)
        res_fp = f"{yt.current_dir}/results"

        if not os.path.exists(res_fp):
            os.makedirs(res_fp)

        data = {
            "data": {
                "url": url,
                "name": yt.fn,
                "text": result
            }
        }

        with open(f"{res_fp}/large_weights_.json", 'a') as f:
            json.dump(data, f, indent=2)

        del yt, result
        gc.collect()
