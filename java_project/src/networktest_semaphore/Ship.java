package networktest_semaphore;

import org.javasim.RestartException;
import org.javasim.Scheduler;
import org.javasim.SimulationEntity;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;

public class Ship extends SimulationEntity {
	/*
	 * Typical generated active payload. Owns its own routing (here equal for all
	 * instances) and service times
	 */

	public Ship(double[] stime, int hc) {
		ResponseTime = 0.0;
		ArrivalTime = Scheduler.currentTime();
		ServiceDuration = new double[hc];

		for (int i = 0; i < hc; i++) {
			ServiceDuration[i] = stime[i];
		}
		harborcount = hc;

		try {
			this.activate(); // starts the life cycle immediately on creation
		} catch (SimulationException e) {
		} catch (RestartException e) {
		}
	}

	public void run() {
		try {
			for (int i = 0; i < harborcount; i++) {
				hold(100); // constant transit time between the harbors
				Network.Q[i].get(this);
				hold(ServiceDuration[i]);
				Network.Q[i].release();
			}
			finished();
			terminate(); // all the work is done and control has to be moved away
		} catch (SimulationException e) {
		} catch (RestartException e) {
		}
	}

	public double OperationTime(int i) {
		return ServiceDuration[i];
	}

	public void finished() {
		ResponseTime = Scheduler.currentTime() - ArrivalTime;
		Network.TotalResponseTime += ResponseTime;
		Network.ProcessedJobs++;
	}

	private double ResponseTime;
	private double ArrivalTime;
	private double[] ServiceDuration;
	private int harborcount;

	private SimulationProcess next;

};