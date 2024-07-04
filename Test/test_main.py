import unittest


def load_tests(loader, tests, pattern):
    # 这里的'unit'是包含测试文件的子目录名，相对于当前执行脚本的位置
    suite = unittest.TestLoader().discover('unit', pattern='test_*.py')
    return suite


if __name__ == '__main__':  
    # 使用unittest.TestProgram的默认行为，或者自定义加载器  
    # unittest.main() 会自动调用 sys.argv 来决定测试集，但这里我们自定义加载方式  
    # 如果你想使用默认的命令行参数，可以直接使用 unittest.main()  
    # unittest.main(testLoader=unittest.TestLoader().loadTestsFromModule(__name__))  
    unittest.TextTestRunner(verbosity=2).run(load_tests(unittest.TestLoader(), None, 'test_*.py'))  

    # 注意：上面的 load_tests 函数通常与 unittest.TestProgram 一起使用，通过命令行参数或配置来调用  
    # 如果你从命令行直接运行 test_main.py，上面的代码已经足够