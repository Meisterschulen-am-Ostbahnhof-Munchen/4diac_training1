#!/usr/bin/env python3
"""Deploy fuer den DIDO-Tester (InputOutputTesterButton_DIDO_OPC_UA) auf eine
Trainings-Platine: Bootfile + Libs-Manifest + ELFs wie
make_4diac_training1_deploy.py, zusaetzlich VT-Pool (DefaultPool.iop),
Sichtbarkeitstabelle (DefaultPool.vis.json) und Web-Client
(apixon-diodo.html), alles nach /data/ des Knotens.

Nutzt die Upload-Logik von make_4diac_training1_deploy.py unveraendert
(Hash-Vergleich, alte Bootfiles/Manifeste aufraeumen, Architektur per
/deviceinfo/), nur mit eigener Dateiliste und eigenem Ziel.

Aufruf: python make_4diac_training1_deploy_dido.py [host]
        host Standard logibus.local (Trainings-Platine per mDNS).

Baut selbst nichts: Bootfile (4diac IDE), Pool (ISO-Designer) und Web-Client
(npm run build) muessen vorher aktuell sein. Rebootet NICHT.
"""

from __future__ import annotations

import sys

import deploy_common
import make_4diac_training1_deploy as deploy

DEFAULT_HOST = "logibus.local"

DIDO_FILES: dict[str, str] = {
    "test_AX_FORTE_PC_AX.fboot": "boot-files/test_AX_FORTE_PC_AX.fboot",
    "DefaultPool.iop": "ISO-DesignerProjects/Workspace_DIDO/DefaultPool/Output/DefaultPool.iop",
    "DefaultPool.vis.json": "ISO-DesignerProjects/Workspace_DIDO/DefaultPool/Output/DefaultPool.vis.json",
    "apixon-diodo.html": "Web-Clients/apixon-diodo-client/dist/apixon-diodo.html",
}


def main(argv: list[str]) -> int:
    host = argv[0] if argv else DEFAULT_HOST
    # REPO_PATHS ist dasselbe dict-Objekt in deploy_common und im Deploy-Modul
    # (resolve_local_path liest es aus deploy_common) - in place ergaenzen.
    deploy_common.REPO_PATHS.update(DIDO_FILES)
    deploy.NODE_BASES = {host: list(DIDO_FILES)}
    deploy.NODE_ORDER = [host]
    return deploy.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
