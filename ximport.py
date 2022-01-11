import os

from dotenv import load_dotenv
from ximport.files import ImportFile
from ximport.arguments import get_args


if __name__ == "__main__":
    load_dotenv()
    args = get_args()
    print(args)
