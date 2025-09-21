# Photo-Watermark

## 简介
Photo-Watermark 是一个命令行图片批量水印工具，可自动读取图片 EXIF 拍摄时间（年月日），并将其作为水印添加到图片上。所有参数均通过交互输入，操作简单直观。

## 功能特性
- 支持 JPEG、PNG 格式图片
- 自动读取 EXIF 拍摄时间作为水印
- 支持自定义字体大小、颜色和水印位置（交互输入）
- 支持批量处理目录下所有图片
- 处理后图片保存在原目录的 _watermark 子目录中

## 使用方法
1. 安装依赖：
	```bash
	pip install -r requirements.txt
	```
2. 运行程序：
	```bash
	python photo_watermark.py
	```
3. 按提示依次输入：
	- 图片文件或目录路径
	- 字体大小（如 30）
	- 字体颜色（如 #FF0000 或 red）
	- 水印位置（top-left、top-right、bottom-left、bottom-right、center）

## 输出目录结构示例
```
D:\photos\
  ├─ img1.jpg
  ├─ img2.jpg
  └─ _watermark\
		  ├─ img1.jpg
		  └─ img2.jpg
```

## 注意事项
- 仅处理有 EXIF 拍摄时间的图片，无 EXIF 的图片会被跳过。
- 字体文件建议使用系统自带的 Arial，若字体显示异常可自行调整代码。
- 支持的颜色格式：#RRGGBB 或常见英文色名（red、green、blue、white、black）。

---
如有问题欢迎反馈。
