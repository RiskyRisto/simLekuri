package networktest;



import org.javasim.RestartException;
import org.javasim.Scheduler;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;

public class Ship extends SimulationProcess {

	public Ship(double[] stime, int hc) {
		ResponseTime = 0.0;
		ArrivalTime = Scheduler.currentTime();
		ServiceDuration = new double[hc];

		for (int i = 0; i < hc; i++) {
			ServiceDuration[i] = stime[i];
		}
		harborcount = hc;

		try {
			this.activate();
		} catch (SimulationException e) {
		} catch (RestartException e) {
		}
	}

	public void run() {
		try {
			for (int i = 0; i < harborcount; i++) {
				get(Network.Q[i]);
				hold(ServiceDuration[i]);
				release(Network.Q[i]);
				hold(10);
			}
			finished();
			cancel();
		} catch (SimulationException e) {
		} catch (RestartException e) {
		}

	}

	public void get(Resource R) {
		if (!R.Reserve(this)) // if we get blocked by the Resource
		{
			try {
				passivate();
			} catch (RestartException e) {
			}
		}
	}

	public void release(Resource R) {
		next = R.Liberate();
		if (!(next == null)) {
			try {
				next.activate();
			} catch (RestartException e) {
			} catch (SimulationException e) {
			}
		}
	}

	public double OperationTime(int i) {
		return ServiceDuration[i];
	}

	public void finished() {
		ResponseTime = Scheduler.currentTime() - ArrivalTime;
		Network.TotalResponseTime += ResponseTime;
		Network.ProcessedJobs++;
//		for (int i=0; i< harborcount; i++) {Servicetime+=ServiceDuration[i];}
//		System.out.println(ResponseTime+" "+ (ResponseTime- harborcount*10 - Servicetime));
	}

	private double ResponseTime;
	private double ArrivalTime;
	private double[] ServiceDuration;
	private int harborcount;
	private double Servicetime = 0.;

	private SimulationProcess next;

};