package networktest_semaphore;

import org.javasim.RestartException;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;

public class Reporter extends SimulationProcess {
	public Reporter(long interval, int hc) {
		check = interval;
		busy = new long[hc];
		harborcount = hc;
	}

	public void run() {
		for (;;) {
			try {
				hold(check);
			} catch (SimulationException e) {
			} catch (RestartException e) {
			}

			checkcount++;
			for (int i = 0; i < harborcount; i++) {
				busy[i] += Network.Q[i].numberWaiting();
			}
		}
	}

	public void report() {
		System.out.println("Checks " + checkcount);
		for (int i = 0; i < harborcount; i++) {
			System.out.println(i + " " + busy[i]);
		}

	}

	public void restart() {
		checkcount = 0;
		for (int i = 0; i < harborcount; i++) {
			busy[i] = 0;
		}

	}

	private long checkcount;
	private long check;
	private long[] busy;
	private int harborcount;

}