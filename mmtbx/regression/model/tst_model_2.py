from __future__ import absolute_import, division, print_function
import mmtbx.model
import libtbx.load_env
import iotbx.pdb
import time
from libtbx.utils import null_out
from cctbx import crystal, adptbx
from six.moves import range
from libtbx.test_utils import approx_equal
from scitbx.array_family import flex

pdb_str_1 = """
CRYST1   79.110   79.110   37.465  90.00  90.00  90.00 P 43 21 2
ATOM      1  N   GLY A  67      11.351   9.426  29.699  1.00 16.57      A    N
ATOM      2  CA  GLY A  67      12.344   8.654  30.419  1.00 16.65      A    C
ATOM      3  C   GLY A  67      13.703   9.318  30.525  1.00 17.27      A    C
ATOM      4  O   GLY A  67      14.613   8.754  31.138  1.00 18.12      A    O
ATOM      5  HA2 GLY A  67      11.164   8.290  32.128  1.00 16.65      A    H
ATOM      6  HA3 GLY A  67      12.899   8.562  30.893  1.00 16.65      A    H
ATOM      7  N   ARG A  68      13.850  10.509  29.946  1.00 17.04      A    N
ATOM      8  CA  ARG A  68      15.122  11.232  30.010  1.00 18.21      A    C
ATOM      9  C   ARG A  68      14.955  12.712  30.337  1.00 19.28      A    C
ATOM     10  O   ARG A  68      15.856  13.506  30.060  1.00 18.39      A    O
ATOM     11  CB  ARG A  68      15.888  11.102  28.683  1.00 17.72      A    C
ATOM     12  CG  ARG A  68      15.297  11.878  27.495  1.00 17.98      A    C
ATOM     13  CD  ARG A  68      16.259  11.919  26.349  1.00 18.60      A    C
ATOM     14  NE  ARG A  68      15.794  12.838  25.306  1.00 17.24      A    N
ATOM     15  CZ  ARG A  68      16.143  12.775  24.023  1.00 19.10      A    C
ATOM     16  NH1 ARG A  68      16.951  11.815  23.586  1.00 18.15      A    N
ATOM     17  NH2 ARG A  68      15.667  13.670  23.169  1.00 19.17      A    N
ATOM     18  HA  ARG A  68      15.977  11.764  31.624  1.00 18.21      A    H
ATOM     19  HB2 ARG A  68      17.228  11.790  28.507  1.00 17.72      A    H
ATOM     20  HB3 ARG A  68      16.065   9.301  28.834  1.00 17.72      A    H
ATOM     21  HG2 ARG A  68      14.632  11.422  26.483  1.00 17.98      A    H
ATOM     22  HG3 ARG A  68      15.102  11.944  27.956  1.00 17.98      A    H
ATOM     23  HD2 ARG A  68      17.713  11.903  27.452  1.00 18.60      A    H
ATOM     24  HD3 ARG A  68      17.031  10.479  25.184  1.00 18.60      A    H
ATOM     25  H  AARG A  68      13.747  10.274  28.969  0.50 17.04      A    H
ATOM     26  HE AARG A  68      14.652  14.091  26.079  0.50 17.24      A    H
ATOM     27 HH11AARG A  68      16.935  11.771  24.831  0.50 18.15      A    H
ATOM     28 HH12AARG A  68      17.117  12.550  21.627  0.50 18.15      A    H
ATOM     29 HH21AARG A  68      14.846  14.096  22.818  0.50 19.17      A    H
ATOM     30 HH22AARG A  68      15.127  14.548  23.046  0.50 19.17      A    H
ATOM     31  D  BARG A  68      12.950  10.336  30.200  0.50 17.04      A    D
ATOM     32  DE BARG A  68      14.587  13.771  24.772  0.50 17.24      A    D
ATOM     33 DH11BARG A  68      16.347  11.268  24.478  0.50 18.15      A    D
ATOM     34 DH12BARG A  68      16.772  11.748  23.372  0.50 18.15      A    D
ATOM     35 DH21BARG A  68      14.983  15.028  23.897  0.50 19.17      A    D
ATOM     36 DH22BARG A  68      15.963  14.351  21.579  0.50 19.17      A    D
ATOM     37  N   THR A  69      13.811  13.085  30.907  1.00 18.60      A    N
ATOM     38  CA  THR A  69      13.578  14.468  31.314  1.00 21.27      A    C
ATOM     39  C   THR A  69      13.418  14.522  32.825  1.00 23.37      A    C
ATOM     40  O   THR A  69      12.315  14.330  33.336  1.00 22.36      A    O
ATOM     41  CB  THR A  69      12.332  15.076  30.647  1.00 18.85      A    C
ATOM     42  OG1 THR A  69      12.366  14.826  29.239  1.00 16.82      A    O
ATOM     43  CG2 THR A  69      12.281  16.578  30.889  1.00 22.56      A    C
ATOM     44  HA  THR A  69      14.647  15.056  30.363  1.00 21.27      A    H
ATOM     45  HB  THR A  69      11.388  15.356  31.910  1.00 18.85      A    H
ATOM     46 HG21 THR A  69      11.173  17.433  30.334  1.00 22.56      A    H
ATOM     47 HG22 THR A  69      12.747  16.477  32.550  1.00 22.56      A    H
ATOM     48 HG23 THR A  69      12.759  16.559  30.395  1.00 22.56      A    H
ATOM     49  H  ATHR A  69      13.914  11.773  30.712  0.50 18.60      A    H
ATOM     50  HG1ATHR A  69      10.933  14.249  27.986  0.50 16.82      A    H
ATOM     51  D  BTHR A  69      13.543  11.891  30.715  0.50 18.60      A    D
ATOM     52  DG1BTHR A  69      12.128  14.870  28.337  0.50 16.82      A    D
TER
END
"""

pdb_str_2 = """
CRYST1   34.238   35.096   43.858  90.00  90.00  90.00 P 21 21 21    0
ATOM      1  N   LYS A  45       6.154   2.754   1.212  1.00 12.39           N
ATOM      2  C   LYS A  45       7.533   2.537  -0.815  1.00  8.18           C
ATOM      3  O   LYS A  45       8.546   2.217  -1.437  1.00  8.18           O
ATOM      4  CA ALYS A  45       7.469   2.388   0.702  0.18  8.95           C
ATOM      5  CB ALYS A  45       7.820   0.954   1.105  0.18 15.56           C
ATOM      6  CG ALYS A  45       7.880   0.729   2.607  0.18  7.12           C
ATOM      7  CD ALYS A  45       8.227  -0.714   2.935  0.18 22.74           C
ATOM      8  CE ALYS A  45       8.402  -0.914   4.432  0.18 43.83           C
ATOM      9  NZ ALYS A  45       7.134  -0.676   5.175  0.18 58.88           N
ATOM     23  CA BLYS A  45       7.396   2.217   0.670  0.82  9.42           C
ATOM     24  CB BLYS A  45       7.467   0.704   0.891  0.82 15.14           C
ATOM     25  CG BLYS A  45       7.428   0.288   2.352  0.82  9.76           C
ATOM     26  CD BLYS A  45       7.539  -1.221   2.500  0.82 22.13           C
ATOM     27  CE BLYS A  45       6.396  -1.931   1.793  0.82 22.20           C
ATOM     28  NZ BLYS A  45       6.495  -3.411   1.927  0.82 22.09           N
ATOM      0  HA ALYS A  45       8.198   3.068   1.142  0.18  9.42           H   new
ATOM      0  HA BLYS A  45       8.223   2.691   1.198  0.82  9.42           H   new
ATOM      0  HB2ALYS A  45       7.082   0.276   0.676  0.18 15.14           H   new
ATOM      0  HB2BLYS A  45       6.636   0.232   0.368  0.82 15.14           H   new
ATOM      0  HB3ALYS A  45       8.784   0.691   0.670  0.18 15.14           H   new
ATOM      0  HB3BLYS A  45       8.384   0.324   0.441  0.82 15.14           H   new
ATOM      0  HG2ALYS A  45       8.624   1.393   3.047  0.18  9.76           H   new
ATOM      0  HG2BLYS A  45       8.244   0.769   2.891  0.82  9.76           H   new
ATOM      0  HG3ALYS A  45       6.919   0.985   3.054  0.18  9.76           H   new
ATOM      0  HG3BLYS A  45       6.499   0.633   2.806  0.82  9.76           H   new
ATOM      0  HD2ALYS A  45       7.439  -1.372   2.568  0.18 22.13           H   new
ATOM      0  HD2BLYS A  45       8.490  -1.560   2.089  0.82 22.13           H   new
ATOM      0  HD3ALYS A  45       9.145  -0.996   2.419  0.18 22.13           H   new
ATOM      0  HD3BLYS A  45       7.536  -1.486   3.557  0.82 22.13           H   new
ATOM      0  HE2ALYS A  45       8.751  -1.929   4.625  0.18 22.20           H   new
ATOM      0  HE2BLYS A  45       5.446  -1.592   2.207  0.82 22.20           H   new
ATOM      0  HE3ALYS A  45       9.172  -0.237   4.801  0.18 22.20           H   new
ATOM      0  HE3BLYS A  45       6.398  -1.661   0.737  0.82 22.20           H   new
ATOM      0  HZ1ALYS A  45       7.263  -0.936   6.174  0.18 22.09           H   new
ATOM      0  HZ1BLYS A  45       5.698  -3.859   1.432  0.82 22.09           H   new
ATOM      0  HZ2ALYS A  45       6.877   0.330   5.110  0.18 22.09           H   new
ATOM      0  HZ2BLYS A  45       7.390  -3.738   1.510  0.82 22.09           H   new
ATOM      0  HZ3ALYS A  45       6.375  -1.255   4.761  0.18 22.09           H   new
ATOM      0  HZ3BLYS A  45       6.467  -3.671   2.934  0.82 22.09           H   new
TER
END
"""

def run():
  if (not libtbx.env.has_module("reduce")):
    print("Reduce not installed, needed for model.idealize_h_minimization(). skipping")
    return
  for pdb_str in [pdb_str_1, pdb_str_2]:
    for use_neutron_distances in [True, False]:
      print("use_neutron_distances:", use_neutron_distances, "*"*30)
      params = mmtbx.model.manager.get_default_pdb_interpretation_params()
      params.pdb_interpretation.use_neutron_distances = use_neutron_distances
      inp = iotbx.pdb.input(lines=pdb_str, source_info=None)
      m = mmtbx.model.manager(
        model_input = inp,
        log         = null_out())
      m.process(pdb_interpretation_params=params, make_restraints=True)
      r1 = m.geometry_statistics()
      #m.setup_riding_h_manager()
      m.idealize_h_minimization(show=False)
      r2 = m.geometry_statistics()
      print("%6.3f %6.3f %6.3f %6.3f"%(
        r1.angle().mean,r1.bond().mean, r2.angle().mean,r2.bond().mean))
      assert r2.angle().mean < 1.0, "assertion %f < 1.0" % r2.angle().mean
      assert r2.bond().mean < 0.01, "assertion %f < 0.01" % r2.bond().mean

def exercise_2():
  inp = iotbx.pdb.input(lines=pdb_str_1, source_info=None)
  model = mmtbx.model.manager(
      model_input = inp)
  model.setup_scattering_dictionaries(scattering_table="wk1995")
  g_stat = model.geometry_statistics()

def exercise_3():
  """
  Make sure model can do deep_copy() straight away.
  """
  inp = iotbx.pdb.input(lines=pdb_str_1, source_info=None)
  model = mmtbx.model.manager(
      model_input = inp)
  new_model = model.deep_copy()

pdb_str_3 = """CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1
SCALE1      0.050000  0.000000  0.000000        0.00000
SCALE2      0.000000  0.050000  0.000000        0.00000
SCALE3      0.000000  0.000000  0.050000        0.00000
ATOM      1  CA  GLY A   1       0.000   0.000   0.000  1.00 30.00           C
ATOM      2  CA  GLY A   2       1.000   1.000   1.000  1.00 30.00           C
ATOM      3  CA  GLY A   3       2.000   2.000   2.000  1.00 30.00           C
ATOM      4  CA  GLY A   4       3.000   3.000   3.000  1.00 30.00           C
ATOM      5  CA  GLY A   5       4.000   4.000   4.000  1.00 30.00           C
ATOM      6  CA  GLY A   6       5.000   5.000   5.000  1.00 30.00           C
ATOM      7  CA  GLY A   7       6.000   6.000   6.000  1.00 30.00           C
ATOM      8  CA  GLY A   8       7.000   7.000   7.000  1.00 30.00           C
ATOM      9  CA  GLY A   9       8.000   8.000   8.000  1.00 30.00           C
ATOM     10  CA  GLY A  10       9.000   9.000   9.000  1.00 30.00           C
TER
END
"""

def exercise_convert_to_isotropic():
  pdb_str = """
ATOM    104  N   SER A   8      14.526  19.060  18.223  1.00  5.10           N
ANISOU  104  N   SER A   8      500    632    808   -107     58    104       N
ATOM    105  CA  SER A   8      14.099  17.792  18.758  1.00  5.95           C
"""
  cs = crystal.symmetry((5.01, 5.01, 5.47, 90, 90, 120), "P 62 2 2")
  pdb_inp = iotbx.pdb.input(source_info=None, lines=pdb_str)
  model = mmtbx.model.manager(
    model_input      = pdb_inp,
    crystal_symmetry = cs)
  #
  m = model.deep_copy()
  m.convert_to_isotropic()
  assert approx_equal(
    m.get_hierarchy().atoms().extract_b(), [5.105875, 5.95])
  assert approx_equal(
    m.get_hierarchy().atoms().extract_uij(),
    [(-1.0, -1.0, -1.0, -1.0, -1.0, -1.0), (-1.0, -1.0, -1.0, -1.0, -1.0, -1.0)])
  #
  m = model.deep_copy()
  m.convert_to_isotropic(selection=flex.bool([False, True]))
  assert approx_equal(
    m.get_hierarchy().atoms().extract_b(),
    model.get_hierarchy().atoms().extract_b())
  assert approx_equal(
    m.get_hierarchy().atoms().extract_uij(),
    model.get_hierarchy().atoms().extract_uij())
  #
  m1 = model.deep_copy()
  m2 = model.deep_copy()
  m1.convert_to_isotropic(selection=flex.bool([True, False]))
  m2.convert_to_isotropic()
  assert approx_equal(
    m1.get_hierarchy().atoms().extract_b(),
    m2.get_hierarchy().atoms().extract_b())
  assert approx_equal(
    m1.get_hierarchy().atoms().extract_uij(),
    m2.get_hierarchy().atoms().extract_uij())

def exercise_set_b_iso():
  pdb_str = """
ATOM    104  N   SER A   8      14.526  19.060  18.223  1.00  5.10           N
ANISOU  104  N   SER A   8      500    632    808   -107     58    104       N
ATOM    105  CA  SER A   8      14.099  17.792  18.758  1.00  5.95           C
"""
  cs = crystal.symmetry((5.01, 5.01, 5.47, 90, 90, 120), "P 62 2 2")
  uc = cs.unit_cell()
  pdb_inp = iotbx.pdb.input(source_info=None, lines=pdb_str)
  model = mmtbx.model.manager(
    model_input      = pdb_inp,
    crystal_symmetry = cs)
  #
  m = model.deep_copy()
  bs = flex.double([10,20])
  m.set_b_iso(values = bs)
  assert approx_equal(m.get_hierarchy().atoms().extract_b(), [-1.0, 20.0])
  us = m.get_hierarchy().atoms().extract_uij()
  assert approx_equal(us[0], model.get_hierarchy().atoms().extract_uij()[0])
  assert approx_equal(us[1], (-1.0, -1.0, -1.0, -1.0, -1.0, -1.0))
  u_iso_1 = m.get_xray_structure().scatterers().extract_u_iso()
  b_iso_2 = m.get_hierarchy().atoms().extract_b()
  assert approx_equal(u_iso_1[0], -1)
  assert approx_equal(b_iso_2[0], -1)
  assert approx_equal(adptbx.u_as_b(u_iso_1[1]), 20)
  assert approx_equal(b_iso_2[1], 20)
  #
  m = model.deep_copy()
  m.convert_to_isotropic()
  bs = flex.double([10,20])
  sel = flex.bool([True, False])
  m.set_b_iso(values=bs, selection=sel)
  assert approx_equal(m.get_b_iso(), [10, 5.95])

def exercise_from_sites_cart():
  from cctbx import crystal
  from scitbx.matrix import col
  from scitbx.array_family import flex
  sites_cart=flex.vec3_double()
  crystal_symmetry=crystal.symmetry(
      unit_cell=(20,20,20,90,90,90),
      space_group_symbol="P 1")
  for i in range(10):
    sites_cart.append(col((i,i,i)))
  model=mmtbx.model.manager.from_sites_cart(sites_cart=sites_cart,
      crystal_symmetry=crystal_symmetry)
  # print model.model_as_pdb()
  for i, a in enumerate(model.get_hierarchy().atoms()):
    assert a.i_seq == i, "iseqs were not set properly"
  assert model.model_as_pdb()==pdb_str_3

def exercise_has_hd():
  inp = iotbx.pdb.input(lines=pdb_str_1, source_info=None)
  m = mmtbx.model.manager(
      model_input               = inp,
      log                       = null_out())
  assert m.has_hd()
  inp = iotbx.pdb.input(lines=pdb_str_3, source_info=None)
  m = mmtbx.model.manager(
      model_input               = inp,
      log                       = null_out())
  assert not m.has_hd()

def exercise_ss_creation_crash():
  pdb_str = """
CRYST1  145.350  135.090  157.320  90.00  90.00  90.00 P 1
SCALE1      0.006880  0.000000  0.000000        0.00000
SCALE2      0.000000  0.007402  0.000000        0.00000
SCALE3      0.000000  0.000000  0.006356        0.00000
ATOM      1  N   ASN A   1      47.095 160.279  31.220  1.00 30.00           N
ATOM      2  CA  ASN A   1      65.985 120.233  34.727  1.00 30.00           C
ATOM      3  C   ASN A   1      56.657 138.700  33.374  1.00 30.00           C
ATOM      4  O   ASN A   1      56.353 138.977  34.561  1.00 30.00           O
ATOM      5  CB  ASN A   1      65.238 120.133  36.068  1.00 30.00           C
ATOM      6  CG  ASN A   1      66.087 119.360  37.057  1.00 30.00           C
ATOM      7  OD1 ASN A   1      65.746 118.217  37.441  1.00 30.00           O
ATOM      8  ND2 ASN A   1      67.240 119.920  37.395  1.00 30.00           N
ATOM      9  N   ASN A   2      56.939 137.441  33.021  1.00 30.00           N
ATOM     10  CA  ASN A   2      67.135 117.384  35.354  1.00 30.00           C
ATOM     11  C   ASN A   2      74.935 104.398  35.546  1.00 30.00           C
ATOM     12  O   ASN A   2      74.423 104.166  34.444  1.00 30.00           O
ATOM     13  CB  ASN A   2      65.828 116.703  35.809  1.00 30.00           C
ATOM     14  CG  ASN A   2      66.092 115.518  36.718  1.00 30.00           C
ATOM     15  OD1 ASN A   2      66.641 114.515  36.266  1.00 30.00           O
ATOM     16  ND2 ASN A   2      65.744 115.556  38.000  1.00 30.00           N
ATOM     17  N   ASN A   3      76.102 103.886  35.920  1.00 30.00           N
ATOM     18  CA  ASN A   3      68.960 115.076  35.163  1.00 30.00           C
ATOM     19  C   ASN A   3      86.047  90.376  35.591  1.00 30.00           C
ATOM     20  O   ASN A   3      87.134  90.903  35.535  1.00 30.00           O
ATOM     21  CB  ASN A   3      70.251 115.882  34.903  1.00 30.00           C
ATOM     22  CG  ASN A   3      71.023 116.208  36.192  1.00 30.00           C
ATOM     23  OD1 ASN A   3      70.637 117.096  36.957  1.00 30.00           O
ATOM     24  ND2 ASN A   3      72.106 115.481  36.436  1.00 30.00           N
ATOM     25  OXT ASN A   3      85.912  89.104  36.045  1.00 30.00           O
TER
END


"""
  with open("exercise_ss_creation_crash_model.pdb","w") as fo:
    fo.write(pdb_str)
  from iotbx.data_manager import DataManager
  dm=DataManager()
  params = mmtbx.model.manager.get_default_pdb_interpretation_params()
  params.pdb_interpretation.secondary_structure.enabled=True
  model = dm.get_model('exercise_ss_creation_crash_model.pdb')
  model.process(make_restraints=True,
    pdb_interpretation_params=params)

if (__name__ == "__main__"):
  t0 = time.time()
  exercise_ss_creation_crash()
  exercise_set_b_iso()
  exercise_convert_to_isotropic()
  run()
  exercise_2()
  exercise_3()
  exercise_from_sites_cart()
  exercise_has_hd()
  print("Time: %6.3f"%(time.time()-t0))
