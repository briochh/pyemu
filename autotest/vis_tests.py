import pyemu
import pandas as pd
import numpy as np
from pathlib import Path
import shutil

from autotest.pst_from_tests import ies_exe_path, mf6_exe_path

# test currently relying on presence of constructed interface pst_template
def test_vis(tmp_path):
    """
    Test the visualization utilities in pyemu.
    """
    from pyemu import vis_utils
    from pyemu import os_utils
    from autotest.pst_from_tests import _get_port
    import flopy
    m_d = Path('..', "examples", "pst_template")
    t_d = Path(tmp_path, 'template')
    if t_d.exists():
        shutil.rmtree(t_d)
    shutil.copytree(m_d, t_d)
    pst = pyemu.Pst(str(t_d / "freyberg.pst"))
    pst.pestpp_options['ies_num_reals'] = 10
    pst.write(pst.filename, version=2)
    port = _get_port()
    m_d = t_d.with_name("master")
    shutil.copy(shutil.which(ies_exe_path), t_d)
    shutil.copy(shutil.which(mf6_exe_path), t_d)
    os_utils.start_workers(t_d, "pestpp-ies", "freyberg.pst", num_workers=5,
                           worker_root=t_d.parent,
                           master_dir=m_d, port=port)
    pst = pyemu.Pst(str(m_d / "freyberg.pst"))
    obs = pst.observation_data
    obs.loc[obs.oname=='hds', ['k', 'i', 'j']] = obs.loc[obs.oname=='hds'].obgnme.str.rsplit("_",expand=True, n=3)[[1,2,3]].values
    pst.observation_data = obs
    sim = flopy.mf6.MFSimulation.load(sim_ws=m_d)
    m = sim.get_model("freyberg6")
    mg = m.modelgrid
    mg.set_coord_info(xoff=622241.1904510253, yoff=3343617.741737109, angrot=15.0,
                      crs="epsg:32614")
    m.dis.xorigin = mg.xoffset
    m.dis.yorigin = mg.yoffset
    m.dis.angrot = mg.angrot
    sim.write_simulation()
    vh = vis_utils.VisHandler(pst, wd=m_d)
    pass

if __name__ == '__main__':
    test_vis('test')
