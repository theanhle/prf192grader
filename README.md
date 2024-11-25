### Cấu trúc thư mục bài workshop

```text
se1909ws1/
├── problems/
│   ├── se1909ws1.pdf
│   ├── prob1.c
│   ├── prob2.c
│   └── prob3.c
└── student_solutions/
    ├── invalid_files/
    │    ├── ce123459pro1.c
    │    ├── ce123459Prob2.c
    │    ├── ce123459prob3.c.c
    │    └── ..
    └── valid_files/
         ├── prob1
         │    ├── ce123456prob1.c
         │    ├── ce123457prob1.c
         │    └── ..
         ├── prob2
         │    ├── ce123456prob2.c
         │    ├── ce123457prob2.c
         │    └── ..
         ├── prob3
         │    ├── ce123456prob3.c
         │    ├── ce123457prob3.c
         │    └── ..
         ├── result.json
         ├── result.xlsx
         └── testcases.json    
```
Trong đó:
1. Folder `problems` chứa đề bài (`se1909ws1.pdf`) và các bài giảng viên làm trước để test đề và sinh testcases (`prob1.c`, `prob2.c`, `prob3.c`).
2. Folder `student_solutions` gồm các file testcases, file bài làm của sinh viên, và các file kết quả:
    - `testcases.json`: file testcase
    - Folder `invalid_files` chứa các file bài làm đặt tên sai
    - Folder `valid_files` gồm các sub-folder `prob1`, `prob2`, `prob3`, .. chứa các file bài làm đặt tên đúng
    - Hai file kết quả chấm được sinh ra bởi chương trình chấm tự động
        -  `result.json`: file kết quả chạy các testcase trên source file của sinh viên
        -  `result.xlsx`: file thống kê điểm của sinh viên

### Hướng dẫn nộp bài Workshop trên Edunext

Giả sử mã sinh viên là `ce123456` và có 3 problems trong bài workshop, lần lượt là `problem 1`, `problem 2`, `problem 3`.
1. Tạo một folder `ce123456`.
2. Làm bài trên CodeBlock, làm xong thì copy file `main.c` vào thư mục `ce123456` rồi đổi tên thành `xproby` trong đó `x` là mã sinh viên, `y` là thứ tự của bài trong đề. Ví dụ `ce123456prob1.c`. Giả sử làm xong cả ba bài, folder `ce123456` sẽ có cấu trúc như sau:
   ```text
    ce123456/
    ├── ce123456prob1.c
    ├── ce123456prob2.c
    └── ce123456prob3.c
   ```
4. Vào trong folder `ce123456` **lựa chọn 3 file `.c` rồi thực hiện zip file chứ không zip folder `ce123456`**. Đặt tên file zip là mã sinh viên. Ví dụ `ce123456.zip`. Cấu trúc file zip như sau:
   ```text
    ce123456.zip
    ├── ce123456prob1.c
    ├── ce123456prob2.c
    └── ce123456prob3.c
   ```
6. Cuối cùng, submit file `ce123456.zip` lên Edunext.

### Hướng dẫn nộp bài PE trên PEA

Thực hiện các bước 1, 2 như trong hướng dẫn nộp bài Workshop ở trên. Sau đó submit folder `ce123456`.

### :warning: Lưu ý quan trọng
1. Các bài nộp sai quy định trên sẽ không có điểm.
2. Trong hàm main không được return một số khác 0 vì điều đó có nghĩa là chương trình kết thúc có lỗi. Hệ thống chấm sẽ coi đó là lỗi và không tính điểm.
3. Hệ điều hành cần để chế độ hiển thị phần đuôi file (file extension) để biết file loại nào (.c, .cpp, cbp, ..) và không nộp nhầm hoặc đặt tên thừa (ví dụ ce123456prob1.c.c). (To show file extensions on Windows 11, open File Explorer, and then click View > Show > File Name Extensions)
4. Chỉ sử dụng ngôn ngữ lập trình C, nộp file source code .c, hệ thống không chấm điểm các file source code viết bằng ngôn ngữ khác.
5. Đề bài cho input gì, theo định dạng nào thì dùng hàm đọc dữ liệu (nên dùng hàm scanf) đọc đúng như thế. Không dùng hàm xuất dữ liệu (ví dụ `printf`) để in ra các prompt nhắc người dùng nhập dữ liệu. Ví dụ đề bài yêu cầu nhập vào hai số nguyên `a`, `b` cách nhau bởi dấu cách:
    - Đoạn chương trình sai:
        ```c
        int a, b;

        printf("Enter two integers separated by a space: ");
        scanf("%d %d", &a, &b);
        ```
    - Đoạn chương trình đúng:
        ```c        
        int a, b;

        scanf("%d %d", &a, &b);
        ```
5. Output đầu ra cần in chính xác theo định dạng yêu cầu trong đề bài (bao gồm cả dấu cách, xuống dòng, chữ thường, chữ hoa, ..) mới có điểm. Riêng hai trường hợp ngoại lệ sau vẫn được tính điểm:
    - Có thêm một dấu cách hoặc một ký tự xuống dòng ở dòng cuối cùng trong output đầu ra. Ví dụ: đề bài yêu cầu in ra 5 số từ 1 tới 5 cách nhau bởi dấu cách thì hai đoạn code sau vẫn cho kết quả đúng:
        ```c
        int i;

        for (i = 1; i < 6; i++)
            printf("%d ", i);
        ```
    - Có thêm một dấu cách ở cuối mỗi dòng trong output đầu ra. Ví dụ đề bài yêu cầu in ra ma trận 3 x 3:
      ```text
      1 2 3
      2 3 4
      3 4 5
      ```
      thì đoạn code sau vẫn cho ra kết quả đúng:
      ```c
      int i, j;

      for (i = 1; i < 4; i++)
      {
          for (j = i; j < i + 3; j++)
              printf("%d ", j);
          printf("\n");
      }
      ```
    Đây là Python script phần tính điểm trong hệ thống chấm tự động:
    ```python
    def preprocess(s):
        s = s.replace(" \n", "\n")
        if len(s)  0:
            return s
        if s[-1] in " \n":
            s = s[:-1]
        return s


    def compute_grade(gold_out, out):
        """
        args:
            gold_out: groundtruth answer
            out: student's output
        returns: 1 if the answer is correct, otherwise return 0        
        """        
        
        gold_out = preprocess(gold_out)
        out = preprocess(out)

        return out  gold_out
    ```
6. Input đầu vào của tất cả các testcase đều có ký tự xuống dòng ,`\n`, ở cuối (giống hệt khi sinh viên làm việc với CodeBlock). Sinh viên lưu ý khi sử dụng các function đọc dữ liệu mà đọc cả ký tự \n (ví dụ fgets). Sinh viên nên dùng function đọc có định dạng scanf.
7. Không dùng hàm getch(); khiến chương trình không thể kết thúc cho đến khi ấn phím.
8. Không dùng các thư viện, hàm không chuẩn (non-standard functions), ví dụ: conio.h, strlwr, strupr, strrev, ..
