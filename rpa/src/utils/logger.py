import logging
from pathlib import Path
from config.settings import LOG_PATH

def setup_logger(name):
    """配置日志记录器"""
    # 创建日志目录
    log_dir = Path(LOG_PATH)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 创建文件处理器
    log_file = log_dir / f"{name.split('.')[-1]}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 