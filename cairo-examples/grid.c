#include <cairo.h>
#include <cairo-pdf.h>
#include <math.h>
#include <stdio.h>

/* double M_PI = 3.1415926; */

int main (int argc, char *argv[])
{
    double mm2pt = 72.0 / 25.4;  // 25.4 mm = 1 inch = 72 pt

    /* A2 */
    double a2_width = 420.0, a2_height = 594.0;  // mm

	double x_width = a2_width * mm2pt;
	double y_height = a2_height * mm2pt;

    /* center of arcs */
	double xc = -x_width / 7.0;
	double yc = y_height / 2.0;

    /* radius of inner and out arc */
	double radius_inner = 240.0 * mm2pt;
	double radius_out = 400.0 * mm2pt;
    /* number of rows */
    int n_row = 4;

    /* inner arc length */
    double inner_arc = 360.0 * mm2pt;

    /* angles of left and right edge */
    /* x-axis is 0, y-axis is M_PI/2 */
    double angle1 = -inner_arc/radius_inner/2.0;
	double angle2 = inner_arc/radius_inner/2.0;
    /* number of columns */
    int n_col = 10;


    const char * filename = "grid.pdf";
    /* start drawing */
	cairo_surface_t *surface =
		/* cairo_image_surface_create (CAIRO_FORMAT_ARGB32, x_width, y_height); */
		cairo_pdf_surface_create (filename, x_width, y_height);

	cairo_t *cr =
		cairo_create (surface);

	cairo_set_line_width (cr, 2.0 * mm2pt);

    /* draw arcs */
    for (int i = 0; i < n_row+1; ++i) {
        double radius = radius_inner + (radius_out - radius_inner) / n_row * i;
        cairo_arc (cr, xc, yc, radius, angle1, angle2);
        cairo_stroke (cr);
    }

    /* draw radius */
    for (int j = 0; j < n_col + 1; ++j) {
        double angle = angle1 + (angle2 - angle1) / n_col * j;
        double x_in = xc + radius_inner * cos(angle);
        double y_in = yc + radius_inner * sin(angle);
        cairo_move_to(cr, x_in, y_in);
        double x_out = xc + radius_out * cos(angle);
        double y_out = yc + radius_out * sin(angle);
        cairo_line_to(cr, x_out, y_out);
        cairo_stroke (cr);
    }


    /* text */
    cairo_text_extents_t extents;
    cairo_select_font_face (cr, "Sans",
            CAIRO_FONT_SLANT_NORMAL,
            CAIRO_FONT_WEIGHT_NORMAL);
    cairo_set_font_size (cr, 72.0);

    char text_buf[16];

    /* left side row markers */
    for (int i = 0; i < n_row; ++i){
        sprintf(text_buf, "%d", i + 1);
        cairo_save(cr);

        double x, y, angle, radius, txc, tyc, text_angle;

        cairo_text_extents (cr, text_buf, &extents);
        angle = angle1 + (angle2 - angle1) / n_col * (-1 + 0.5);
        radius = radius_inner + (radius_out - radius_inner) / n_row * (i + 0.5);
        txc = xc + radius * cos(angle);
        tyc = yc + radius * sin(angle);

        x = - extents.width / 2;
        y = extents.height / 2;

        /* printf("%f %f %f %f\n", extents.width, extents.height, extents.x_bearing, extents.y_bearing); */

        cairo_translate(cr, txc, tyc);
        cairo_rotate(cr, - angle + M_PI);
        cairo_translate(cr, x, y);
        cairo_move_to (cr, 0, 0);
        cairo_show_text(cr, text_buf);
        cairo_restore(cr);
    }

    /* right side row markers */
    for (int i = 0; i < n_row; ++i){
        sprintf(text_buf, "%d", i + 1);
        cairo_save(cr);

        double x, y, angle, radius, txc, tyc, text_angle;

        cairo_text_extents (cr, text_buf, &extents);
        angle = angle1 + (angle2 - angle1) / n_col * (n_col + 0.5);
        radius = radius_inner + (radius_out - radius_inner) / n_row * (i + 0.5);
        txc = xc + radius * cos(angle);
        tyc = yc + radius * sin(angle);

        x = - extents.width / 2;
        y = extents.height / 2;

        /* printf("%f %f %f %f\n", extents.width, extents.height, extents.x_bearing, extents.y_bearing); */

        cairo_translate(cr, txc, tyc);
        cairo_rotate(cr, - angle);
        cairo_translate(cr, x, y);
        cairo_move_to (cr, 0, 0);
        cairo_show_text(cr, text_buf);
        cairo_restore(cr);
    }

    /* draw colum markers */
    for (int i = 0; i < n_col; ++i){
        sprintf(text_buf, "%d", n_col - i);
        cairo_save(cr);

        double x, y, angle, radius, txc, tyc, text_angle;

        cairo_text_extents (cr, text_buf, &extents);
        angle = angle1 + (angle2 - angle1) / n_col * (i + 0.5);
        radius = radius_inner + (radius_out - radius_inner) / n_row * (-1 + 0.5);
        txc = xc + radius * cos(angle);
        tyc = yc + radius * sin(angle);

        x = - extents.width / 2;
        y = extents.height / 2;

        /* printf("%f %f %f %f\n", extents.width, extents.height, extents.x_bearing, extents.y_bearing); */

        cairo_translate(cr, txc, tyc);
        cairo_rotate(cr, angle - M_PI/2);
        cairo_translate(cr, x, y);
        cairo_move_to (cr, 0, 0);
        cairo_show_text(cr, text_buf);
        cairo_restore(cr);
    }






    /* finishing */
    cairo_destroy (cr);
	/* cairo_surface_write_to_png (surface, "hello.png"); */
	cairo_surface_destroy (surface);

	return 0;
}
