# download LSL and pylsl from https://code.google.com/p/labstreaminglayer/
# Eg: ftp://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl-Python-1.10.2.zip
# put in "lib" folder (same level as user.py)
import sys; sys.path.append('lib') # help python find pylsl relative to this example program

from pylsl import StreamInfo, StreamOutlet
import plugin_interface as plugintypes

# Use LSL protocol to broadcast data using one stream for EEG and one stream for AUX
class StreamerLSL(plugintypes.IPluginExtended):
	# From IPlugin
	def activate(self):
		eeg_stream = "OpenBCI_EEG"
		eeg_id = "openbci_eeg_id1"
		aux_stream = "OpenBCI_AUX"
		aux_id = "openbci_aux_id1"
		
		if len(self.args) > 0:
			eeg_stream = self.args[0]
		if len(self.args) > 1:
			eeg_id = self.args[1]
		if len(self.args) > 2:
			aux_stream = self.args[2]
		if len(self.args) > 3:
			aux_id = self.args[3]

		# Create a new streams info, one for EEG values, one for AUX (eg, accelerometer) values
		print "Creating LSL stream for EEG. Name:", eeg_stream, "- ID:", eeg_id, "- data type: float32.", self.eeg_channels, "channels at", self.sample_rate, "Hz."
		info_eeg = StreamInfo(eeg_stream, 'EEG', self.eeg_channels,self.sample_rate,'float32',eeg_id);
		# NB: set float32 instead of int16 so as OpenViBE takes it into account
		print "Creating LSL stream for AUX. Name:", aux_stream, "- ID:", aux_id, "- data type: float32.", self.aux_channels, "channels at", self.sample_rate, "Hz."
		info_aux = StreamInfo(aux_stream, 'AUX', self.aux_channels,self.sample_rate,'float32',aux_id);
		
		# make outlets
		self.outlet_eeg = StreamOutlet(info_eeg)
		self.outlet_aux = StreamOutlet(info_aux)
	    
	# send channels values
	def __call__(self, sample):
		self.outlet_eeg.push_sample(sample.channel_data)
		self.outlet_aux.push_sample(sample.aux_data)

	def show_help(self):
	  	print """Optional arguments: [EEG_stream_name [EEG_stream_ID [AUX_stream_name [AUX_stream_ID]]]]
	  	\t Defaults: "OpenBCI_EEG" / "openbci_eeg_id1" and "OpenBCI_AUX" / "openbci_aux_id1"."""
