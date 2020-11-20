package surgery;

/*
 * constants used in simulation
 */
public final class Settings {
	public static final int N_PREPARATION_ROOMS = 3;
	public static final int N_OPERATION_ROOMS = 1;
	public static final int N_RECOVERY_ROOMS = 3;

	// minutes
	public static final int MEAN_INTERARRIVAL_TIME = 25;
	public static final int MEAN_PREPARATION_TIME = 40;
	public static final int MEAN_OPERATION_TIME = 20;
	public static final int MEAN_RECOVERY_TIME = 40;

	// public static final int WEEKS = 12;
	// public static final double SIMULATION_TIME = 60 * 24 * 7 * WEEKS;
	public static final double SIMULATION_TIME = 1000.0;

	public static final int N_SAMPLES = 20;

	public static final double CANCELLATION_PROBABILITY = 0.05;

	private Settings() {
	}

}
