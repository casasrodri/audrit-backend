from controllers import BaseController
from database import SqlDB
from entidades.controles.controller import ControlesController
from entidades.riesgos.controller import RiesgosController


class LinksController(BaseController):

    def asociar_control_riesgo(db: SqlDB, control_id: int, riesgo_id: int):
        control = ControlesController.get(db, control_id)
        riesgo = RiesgosController.get(db, riesgo_id)

        if control not in riesgo.controles:
            riesgo.controles.append(control)

        if riesgo not in control.riesgos:
            control.riesgos.append(riesgo)

        db.commit()

        return {"status": "ok"}
