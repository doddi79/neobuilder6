from neobuilder6.neobuilder import NeoBuilder


if __name__ == '__main__':
    #n = NeoBuilder(
    #    package='efrit',
    #    protopath='./_sandbox/proto/',
    #    build_root='./_sandbox/build/',
    #    verbose=True,
    #)
    n = NeoBuilder(
        package='sandbox',
        protopath='./tests/res2/proto',
        build_root='./_sandbox/build/',
        verbose=True,
    )
    n.build()
