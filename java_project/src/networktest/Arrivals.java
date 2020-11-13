package networktest;

import java.io.IOException;

import org.javasim.RestartException;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;
import org.javasim.streams.RandomStream;

public class Arrivals extends SimulationProcess {

	public Arrivals(RandomStream inter, RandomStream[] st, int hc) {
		InterArrivalTime = inter;
		servicetime = new RandomStream[hc];
		servtime = new double[hc];
		servicetime = st;
		harborcount = hc;
	}

	public void run() {
		for (;;) {
			try {
				for (int i = 0; i < harborcount; i++) {
					servtime[i] = servicetime[i].getNumber();
				}
				Ship work = new Ship(servtime, harborcount);
				hold(InterArrivalTime.getNumber());
			} catch (SimulationException e) {
			} catch (RestartException e) {
			} catch (IOException e) {
			}
		}
	}

	private RandomStream InterArrivalTime;
	private RandomStream[] servicetime;
	private double[] servtime;
	private int harborcount;
};