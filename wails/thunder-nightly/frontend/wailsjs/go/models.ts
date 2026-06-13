export namespace main {
	
	export class RepoInfo {
	    Name: string;
	    FullName: string;
	    Description: string;
	    Stars: number;
	    Forks: number;
	    Language: string;
	    LicenseName: string;
	    URL: string;
	    DefaultBranch: string;
	    OpenIssues: number;
	    Watchers: number;
	
	    static createFrom(source: any = {}) {
	        return new RepoInfo(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Name = source["Name"];
	        this.FullName = source["FullName"];
	        this.Description = source["Description"];
	        this.Stars = source["Stars"];
	        this.Forks = source["Forks"];
	        this.Language = source["Language"];
	        this.LicenseName = source["LicenseName"];
	        this.URL = source["URL"];
	        this.DefaultBranch = source["DefaultBranch"];
	        this.OpenIssues = source["OpenIssues"];
	        this.Watchers = source["Watchers"];
	    }
	}

}

