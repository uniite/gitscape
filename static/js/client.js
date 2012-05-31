var compiledCommitTemplate;
var theRepo;

$(function() {
    theRepo = new RepoModel({});
    theRepo.loadBranches();
    theRepo.loadRepos();
    ko.applyBindings(theRepo);
});

function getDate(timestamp) {
    var d = new Date(0);
    d.setUTCSeconds(timestamp);
    return d;
}

function scrollToCommit(sha) {
    $('html, body').stop().animate({
       scrollTop: $("a[name=" + sha + "]").offset().top - 40
    });
}

var commits = {};
var selectedCommits = [];

var CommitModel = function(data, repo) {
    var self = this;
    ko.mapping.fromJS(data, {}, this);

    this.selected = ko.observable(false);


    this.link = ko.computed(function() {
        return "https://github.com/eachscape/builder/commit/" + this.hexsha();
    }, this);

    this.scrollTo = function(commit) {
        $("#command a").click(function(e) {
            $("html, body").stop().animate({
               scrollTop: $("a[name={0}]".format(commit.hexsha())).offset().top + 90
            });
            e.preventDefault();
        });
    }

    this.select = function() {
        if (this.selected()) {
            this.selected(false);
            repo.selectedCommits.remove(this);
        } else {
            this.selected(true);
            repo.selectedCommits.push(this);
        }
    }

    this.shortMessage = ko.computed(function() {
        var lines = this.message().split("\n");
        if (lines.length > 1) {
            return lines[0] + "...";
        } else {
            return lines[0];
        }
    }, this);

    this.isUpstream = ko.computed(function() {
        return this.branch() == "origin/live";
    }, this);
}

var RepoModel = function(data) {
    var self = this;
    ko.mapping.fromJS(data, {}, this);

    this.clearSelectedCommits = function() {
        while (self.selectedCommits().length > 0) {
            self.selectedCommits()[0].select();
        }
    }


    this.commits = ko.observableArray();


    this.branchDiff = function() {
        self.selectedCommits([]);
        $("#loader").show();
        $("#commits .content, #footer").hide();
        ajaxCall("branch_diff", {
            base: self.base(),
            upstream: self.upstream()
        }, loadCommits);
    }
    this.loadBranches = function() {
        $("#commits").hide();
        ajaxCall("branches", {}, function(data) {
            ko.mapping.fromJS(data, {}, self);
            $("#commits").fadeIn();
            theRepo.branchDiff();
        });
    }
    this.loadRepos = function() {
        ajaxCall("repos", {}, function(data) {
            self.repos(data);
            self.currentRepo(self.repos()[0]);
        });
    }

    this.setBase = function(branch) {
        self.base(branch);
        self.branchDiff();
    }
    this.setRepo = function(repoPath) {
        ajaxCall("set_repo", {path: repoPath}, function(data) {
            if (data === true) {
                self.currentRepo(repoPath);
                self.loadBranches();
            } else {
                alert("Could not switch repos");
            }
        });
    }
    this.setUpstream = function(branch) {
        self.upstream(branch);
        self.branchDiff();
    }

    this.base = ko.observable();
    this.branches = ko.observable();
    this.currentRepo = ko.observable();
    this.repos = ko.observableArray();
    this.selectedCommits = ko.observableArray();
    this.upstream = ko.observable();

    this.gitCommand = ko.computed(function() {
        if (this.selectedCommits().length == 0) {
            return "Select some commits";
        } else {
            return "git cherry-pick " + this.selectedCommits().join(" ");
        }
    }, this);
};



function loadCommits(data) {
    var commits = data.commits;
    for (var i in commits) {
        commits[i].authored_date = strftime('%B %d, %Y %l:%M:%S%P', getDate(commits[i].authored_date));
    }
    var mapping = {
        commits: {
            create: function(options) {
                return new CommitModel(options.data, theRepo);
            }
        }
    };
    theRepo.commits(ko.mapping.fromJS(data, mapping).commits());
    $("#loader").hide();
    $("#commits .content, #footer").fadeIn();
}

function ajaxCall(path, args, callback) {
    $.get("/" + path, args, function(data) {
       callback(JSON.parse(data));
    });
}
