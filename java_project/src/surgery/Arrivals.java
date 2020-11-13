package surgery;

import java.io.IOException;

import org.javasim.RestartException;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;
import org.javasim.streams.ExponentialStream;

public class Arrivals extends SimulationProcess {
	private ExponentialStream interarrivalTime = new ExponentialStream(25);
	private ExponentialStream preparationTime = new ExponentialStream(40);
	private ExponentialStream operationTime = new ExponentialStream(20);
	private ExponentialStream recoveryTime = new ExponentialStream(40);
	
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
