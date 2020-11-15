package surgery;

/**
 * Run simulation
 * Print information
 * @author Juha Reinikainen
 *
 */
public class Main {
	public static void main(String[] args) {
		Surgery surgery = new Surgery();
		
		surgery.await();

		System.out.println("Simulating operation of surgery facilities for " + Settings.WEEKS + " weeks");
		
		System.out.println("departed in total " + Surgery.nDeparted);
		
		long cancelledOperations = Surgery.operationsCancelled;
		System.out.println("Number of operations cancelled " + cancelledOperations);
		
		//Average throughput time
		double mtt = Surgery.tTotal / Surgery.nDeparted;
		System.out.println("Average throughput time " + mtt);

		//Average blocking time
		double mbt = Surgery.tRecoveryWaiting / Surgery.nWaited;
		System.out.println("Average blocking time for recovery " + mbt);

		//average length of the queue at entrance 
		double mqlae = Surgery.nQeueued / Surgery.nTotal;
		System.out.println("Average length of the queue at entrance " + mqlae);

		//utilization of the operation theatre
		double ur = Surgery.tBusy / Settings.SIMULATION_TIME;
		System.out.println("Utilization rate of the operation theatre " + ur);
		
		System.exit(0);
	}
}
