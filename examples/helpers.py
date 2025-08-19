import os
import pyemu

def process_model_outputs():
	import numpy as np
	print("processing model outputs")
	arr = np.random.random(100)
	np.savetxt("special_outputs.dat",arr)
	return arr


def write_ins_file(d):
	cwd = os.getcwd()
	os.chdir(d)
	arr = process_model_outputs()
	os.chdir(cwd)
	with open(os.path.join(d,"special_outputs.dat.ins"),'w') as f:
		f.write("pif ~\n")
		for i in range(arr.shape[0]):
			f.write("l1 !sobs_{0}!\n".format(i))

	
	i = pyemu.pst_utils.InstructionFile(os.path.join(d,"special_outputs.dat.ins"))
	df = i.read_output_file("special_outputs.dat")
	
	return df


def hds2csv(d='.'):
    import flopy
    from pathlib import Path
    import numpy as np
    hfile = list(Path(d).glob('*.hds'))[0]
    hds = flopy.utils.binaryfile.HeadFile(hfile)
    for n, (kstp, kper) in enumerate(hds.get_kstpkper()):
        # get the head data
        head = hds.get_data(kstpkper=(kstp, kper))
        for k, hdk in enumerate(head):
            np.savetxt(Path(d, f'hds_{kper}_{kstp}_{k}.csv'), hdk)


if __name__ == "__main__":
	#process_model_outputs()
	write_ins_file(".")
	