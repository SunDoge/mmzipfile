# mmzipfile

## Install

If in China

```shell
pip install -U git+https://hub.fastgit.org/SunDoge/mmzipfile.git
```

else

```shell
pip install -U git+https://github.com/SunDoge/mmzipfile.git
```

## Usage

### 打包

```shell
zip -r -0 zip_file_name.zip your_data_dir/
```

或者

```shell
mmzipfile your_data_dir zip_file_name.zip
```

### 读取

check [example/read_imagenette.py](example/read_imagenette.py)
