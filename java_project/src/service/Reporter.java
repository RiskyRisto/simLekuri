package service;

import org.javasim.*;

public class Reporter extends SimulationProcess {
	public Reporter(long interval) {
		check = interval;

	}

	public void run() {
		for (;;) {
			result[exp][checkcount] = MachineShop.TotalResponseTime - oldResponseTime;
			oldResponseTime = MachineShop.TotalResponseTime;
			checkcount++;
			try {
				hold(check);
			} catch (SimulationException e) {
			} catch (RestartException e) {
			}
		}
	}

	public void report(int count) {
		for (int i = 0; i < count; i++) {
			for (int j = 0; j < 10; j++) {
				System.out.print(result[j][i] + " ");
			}
			System.out.println();
		}
	}

	public void reset(int experiment) {
		exp = experiment;
		checkcount = 0;
		oldResponseTime = MachineShop.TotalResponseTime;
	}

	private long check;
	private int checkcount = 0;
	private int exp;
	private double oldResponseTime;
	private double[][] result = new double[10][1000];
}