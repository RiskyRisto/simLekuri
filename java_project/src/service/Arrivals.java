package service;

import org.javasim.*;
import org.javasim.streams.*;

import java.io.IOException;

public class Arrivals extends SimulationProcess {

	public Arrivals(double mean) {
		InterArrivalTime = new ExponentialStream(mean);
	}

	public void run() {
		for (;;) {
			try {
				hold(InterArrivalTime.getNumber());
				Job work = new Job();
				work.activate();
			} catch (SimulationException e) {
			} catch (RestartException e) {
			} catch (IOException e) {
			}

		}
	}

	private ExponentialStream InterArrivalTime;

};