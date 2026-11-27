from flask import Flask, render_template, request, redirect, url_for, flash
from datos import inicializar_bd
import logica_web as logica

app = Flask(__name__)
app.secret_key = "clave_super_secreta_enfermeria_dev"

inicializar_bd()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/camas")
def ver_camas():
    camas = logica.mostrar_camas()
    insumos = logica.mostrar_insumos()
    return render_template("camas.html", camas=camas, insumos=insumos)


@app.route("/internar", methods=["POST"])
def internar():
    numero_cama = request.form.get("numero_cama")
    paciente_nombre = request.form.get("paciente_nombre")
    motivo_internacion = request.form.get("motivo_internacion")

    exito, mensaje = logica.internar_paciente(
        numero_cama, paciente_nombre, motivo_internacion
    )
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("ver_camas"))


@app.route("/alta/<int:numero_cama>", methods=["POST"])
def dar_alta(numero_cama):
    exito, mensaje = logica.dar_alta_paciente(numero_cama)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("ver_camas"))


@app.route("/insumos", methods=["GET", "POST"])
def gestionar_insumos():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        stock = request.form.get("stock")
        descripcion = request.form.get("descripcion", "")
        seguir = request.form.get("seguir_cargando") == "1"

        exito, mensaje = logica.agregar_insumo(nombre, stock, descripcion)
        flash(mensaje, "success" if exito else "danger")

        # Si falló o el usuario eligió "Guardar y cargar otro", volvemos al formulario
        if not exito or seguir:
            return redirect(url_for("gestionar_insumos", cargar="1"))
        return redirect(url_for("gestionar_insumos"))

    insumos = logica.mostrar_insumos()
    mostrar_form = request.args.get("cargar") == "1" or len(insumos) == 0
    return render_template(
        "insumos.html", insumos=insumos, mostrar_form=mostrar_form
    )


@app.route("/insumos/sumar", methods=["POST"])
def sumar_stock():
    nombre = request.form.get("nombre")
    cant_sumar = request.form.get("cant_sumar")

    exito, mensaje = logica.actualizar_stock_insumos(nombre, cant_sumar)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("gestionar_insumos"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)