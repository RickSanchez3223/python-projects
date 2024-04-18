from pathlib import Path
from datetime import datetime

root_path = Path('files/2023/Mar')
for i in range(9, 11):
    file_name = f"f{i}.txt"
    new_path = root_path / Path(file_name)
    new_path.touch()
    new_path.write_text(file_name)

root_dir = Path('files')
print(root_dir.cwd())

for path in root_dir.glob("**/*"):
    if path.is_file():
        parts = path.parts
        new_file_name = f"{parts[-3]}_{parts[-2]}-{parts[-1]}"
        new_file_path = path.with_name(new_file_name)
        path.rename(new_file_path)



path = Path('files/2022/Dec/2022_Dec-f1.txt')
stat = path.stat()
print(stat.st_ctime)
print(datetime.fromtimestamp(stat.st_ctime).strftime("%d-%m-%Y %H:%M:%s"))
