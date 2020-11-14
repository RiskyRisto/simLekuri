package surgery;

import java.io.IOException;

import org.javasim.RestartException;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;
import org.javasim.streams.ExponentialStream;

/*
 * generate patients
 */
public class Arrivals extends SimulationProcess {
	private ExponentialStream interarrivalTime = new ExponentialStream(Settings.MEAN_INTERARRIVAL_TIME);
	private ExponentialStream preparationTime = new ExponentialStream(Settings.MEAN_PREPARATION_TIME);
	private ExponentialStream operationTime = new ExponentialStream(Settings.MEAN_OPERATION_TIME);
	private ExponentialStream recoveryTime = new ExponentialStream(Settings.MEAN_RECOVERY_TIME);
	
	public void run() {
		while (true) {
			try {
				double it = interarrivalTime.getNumber();
				double pt = preparationTime.getNumber();
				double ot = operationTime.getNumber();
				double rt = recoveryTime.getNumber();
				
				//activates self
				new Patient(pt, ot, rt);
				hold(it);
			} catch (RestartException | IOException | SimulationException e) {
				e.printStackTrace();
			}
			
		}
	}

}
