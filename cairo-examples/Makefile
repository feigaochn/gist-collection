CC = cc
CFLAGS = -I/usr/local/Cellar/cairo/1.14.6_1/include/cairo -I/usr/local/Cellar/glib/2.50.0/include/glib-2.0 -I/usr/local/Cellar/glib/2.50.0/lib/glib-2.0/include -I/usr/local/opt/gettext/include -I/usr/local/Cellar/pcre/8.39/include -I/usr/local/Cellar/pixman/0.34.0/include/pixman-1 -I/usr/local/Cellar/fontconfig/2.12.1_2/include -I/usr/local/opt/freetype/include/freetype2 -I/usr/local/Cellar/libpng/1.6.25/include/libpng16 -L/usr/local/Cellar/cairo/1.14.6_1/lib -lcairo

TARGET = grid


# all: $(TARGET)
all: pdf

pdf: $(TARGET)
	./$(TARGET).o

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET).o $(TARGET).c

run: $(TARGET)
	eval $(TARGET)

clean:
	$(RM) $(TARGET).{pdf,o}

