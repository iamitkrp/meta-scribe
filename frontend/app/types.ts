export interface ParseResponse {
	doc_id: string;
	title?: string | null;
	abstract?: string | null;
	methodology?: string | null;
	equations: string[];
	datasets: string[];
}


