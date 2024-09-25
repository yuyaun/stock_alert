# 使用大型映像來構建你的應用程序
FROM python:3.11-slim as builder
WORKDIR /usr/src/app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libev-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 使用官方的Python映像作為基礎
FROM python:3.11-slim
# 設置工作目錄
WORKDIR /usr/src/app
# 設置亞洲台北時區
RUN apt-get update && apt-get install -y tzdata && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY --from=builder /usr/local /usr/local

# 拷貝整個應用程序到容器中
COPY . .
CMD ["python", "twii_alert.py"]

