var app = angular.module('TestSys', ['chieffancypants.loadingBar', 'ngAnimate']);
app.config(function(cfpLoadingBarProvider) {
    cfpLoadingBarProvider.includeSpinner = true;
  })

var INTEGER_REGEXP = /^\-?\d*$/;
app.directive('integer', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue) {
                if (INTEGER_REGEXP.test(viewValue)) {
                    ctrl.$setValidity('integer', true);
                    return viewValue;
                } else {
                    ctrl.$setValidity('integer', false);
                    return undefined;
                }
            });
        }
    };
});

app.filter('trustHtml', function ($sce) {
        return function (input) {
            return $sce.trustAsHtml(input);
        }
    });

app.directive('if', function($parse, $compile){
    var compile = function($element, $attrs){
      var cond = $parse($attrs.true);
      
      var link = function($scope, $ielement, $iattrs, $controller){
        $scope.if_node = $compile($.trim($ielement.html()))($scope, angular.noop);
        $ielement.empty();
        var mark = $('<!-- IF/ELSE -->');
        $element.before(mark);
        $element.remove();
  
        $scope.$watch(function(scope){
          if(cond(scope)){
            mark.after($scope.if_node);
            $scope.else_node.detach();
          } else {
            if($scope.else_node !== undefined){
              mark.after($scope.else_node);
              $scope.if_node.detach();
            }
          }
        });
      }
      return link;
    }
  
    return {compile: compile,
            scope: true,
            restrict: 'E'}
});
  
app.directive('else', function($compile){
	var compile = function($element, $attrs){
	  
	  var link = function($scope, $ielement, $iattrs, $controller){
		$scope.else_node = $compile($.trim($ielement.html()))($scope, angular.noop);
		$element.remove();
	  }
	  return link;
}

	return {compile: compile,
			restrict: 'E'}
});
  
$(function () {
    $('input, textarea').placeholder();
    $('.default-focus').focus();
    $('*').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body"
    });
});

function LoginCtrl($scope, $http) {
    $scope.isMatch = true;
    $scope.isDisabled = false;
    $scope.login = function () {
        $scope.isMatch = true;
        $scope.isDisabled = false;
        $http.post('/Login', $scope.User).success(function (result) {
            if (result.isMatch != null) {
                $scope.isMatch = result.isMatch;
            }
            if (result.isDisabled != null) {
                $scope.isDisabled = result.isDisabled;
            }
            if (result.isMatch != null && result.isMatch) {
                window.location.href = '/MyZone';
            }
        });
    }
}

function RegisterCtrl($scope, $http) {
    $scope.userExist = false;
    $scope.register = function () {
        $scope.userExist = false;
        $http.post('/Register/Save', $scope.User).success(function (result) {
            if (!result.created) {
                $scope.userExist = true;
            }
            else {
                window.location.href = '/MyZone';
            }
        });
    }
}

function ProjectCtrl($scope, $http) {
    $scope.ProjectList = [];
	$scope.TaskList = [];
	$scope.IssueList = [];
	$scope.LogList = [];
    $scope.ProjectQuery = { PageNo: 1, ProjectName: '', Status: 1, RowCount: 0, PageCount: 0 };
	$scope.TaskQuery = { PageNo: 1, ProjectId: -1, TaskName: '', TaskType: -1, AssignTo: -1, New: true, InProgress: true, Completed: false, Canceled: false, RowCount: 0, PageCount: 0 };
	$scope.IssueQuery = { PageNo: 1, ProjectId: -1, Subject: '', AssignTo: -1, CategoryId: -1, Open: true, Fixed: true, Closed: false, Canceled: false, RowCount: 0, PageCount: 0 };
    $scope.LogQuery = { PageNo: 1, RowCount: 0, PageCount: 0 };
	$scope.AddSuccess = false;
	$scope.create = function () {
		$scope.AddSuccess = false;
        $http.post('/Project/NewCreate', $scope.Project).success(function (result) {
            if (result.created) {
				$scope.AddSuccess = true;
				window.location.href = "/MyZone";
            }
        });
    }
    $scope.query = function () {
        $http.post('/Project/Query', $scope.ProjectQuery).success(function (result) {
			$scope.ProjectList = [];
            $scope.ProjectList = result.data;
            $scope.ProjectQuery.RowCount = result.row_count;
            $scope.ProjectQuery.PageCount = result.page_count;
            $scope.ProjectQuery.PageNo = result.page_no;
        });

        $http.post('/Task/Query', $scope.TaskQuery).success(function (result) {
			$scope.TaskList = [];
            $scope.TaskList = result.data;
            $scope.TaskQuery.RowCount = result.row_count;
            $scope.TaskQuery.PageCount = result.page_count;
            $scope.TaskQuery.PageNo = result.page_no;
        });
		
        $http.post('/Issue/Query', $scope.IssueQuery).success(function (result) {
            $scope.IssueList = [];
            $scope.IssueList = result.data;
            $scope.IssueQuery.RowCount = result.row_count;
            $scope.IssueQuery.PageCount = result.page_count;
            $scope.IssueQuery.PageNo = result.page_no;
        });
        
		$http.post('/Project/Log',  $scope.LogQuery).success(function (result) {
			$scope.LogList = [];
            $scope.LogList = result.data;
            $scope.LogQuery.RowCount = result.row_count;
            $scope.LogQuery.PageCount = result.page_count;
            $scope.LogQuery.PageNo = result.page_no;
        });	
    }
}

function ProjectUpdateCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
    $scope.Delete = function () {
        $http.post('/Project/Delete', { ProjectId: $scope.Project.ProjectId }).success(function (result) {
            if (result.deleted) {
                $scope.DeleteSuccess = true;
                window.location.href = '/MyZone';
            }
        });
    }
    $scope.update = function () {
        $http.post('/Project/Update', $scope.Project).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
                window.location.href = '/MyZone';
            }
        });
    }
}

function TaskCtrl($scope, $http) {
    $scope.TaskList = [];
    $scope.Query = { PageNo: 1, ProjectId: -1, TaskName: '', TaskType: -1, AssignTo: 0, New: true, InProgress: true, Completed: false, Canceled: false, RowCount: 0, PageCount: 0 };
    $scope.queryInit = function () {
        $http.post('/Task/Query', $scope.Query).success(function (result) {
            $scope.TaskList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
	
}

function TaskCreateCtrl($scope, $http) {
    $scope.AddSuccess = false;
    editor = UE.getEditor('editor');
    $scope.Task = { TaskName: '', Priority: 2, AssignTo: -1, Description: '', TaskLinkCase: '' };
    $scope.create = function () {
        $scope.Task.Description = editor.getContent();
        $http.post('/Task/CreateNew', $scope.Task).success(function (result) {
            if (result.created) {
                $scope.AddSuccess = true;
                window.location.href = "/Project/Task/" + result.ProjectId;
            }
        });
    }
}

function TaskUpdateCtrl($scope, $http) {
	$scope.ShowUpdate = false;
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
	$scope.Task = {TaskId: 0, ProjectId: 0, TaskName: '', TaskType: -1, Priority: 0, Progress: 0, AssignTo: 0, Status: 0, Effort: 0, Description: '', TaskLinkCase:''};
	$scope.TaskQueryCaseList = [];
	$scope.TaskQueryCase = { ProjectId: -1, TaskId: 0, CaseType: 0};
	$scope.IsCheckAll = false;
	$scope.UserId = 0;
	$scope.RunInfo = {};
	$scope.isExecuted = false;
	$scope.WaveInfo = [];
	$scope.RetWaveInfo = {};
	$scope.LatestWaveId = '';
	$scope.CurrWaveId = '';
	
	$scope.queryInit = function () {
        $http.post('/Task/QuerySingle', { TaskId: $scope.Task.TaskId} ).success(function (result) {
            $scope.Task = result.retTask; 
			$scope.QueryCase();
        });
    }

    $scope.edit = function () {
        $scope.ShowUpdate = !$scope.ShowUpdate;
        editor = UE.getEditor('editor');
		editor.ready(function(){    
			editor.setContent($scope.Task.Description);
		})
    }
	
    $scope.update = function () {
        $scope.Task.Description = editor.getContent();
		var s = '';
		for (var i=0;i<$scope.TaskQueryCaseList.length;i++) {
			if($scope.TaskQueryCaseList[i].IsChecked){
				s = s + $scope.TaskQueryCaseList[i].CaseId.toString()  + ",";
			}
		}
		$scope.Task.TaskLinkCase=s;
        $http.post('/Task/Update', $scope.Task).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
				window.location.href = "/Task/Detail/" + $scope.Task.ProjectId + "_" + $scope.Task.TaskId;
            }
        });
    }

    $scope.Delete = function () {
        $http.post('/Task/Delete', { 'TaskId': $scope.Task.TaskId }).success(function (result) {
            if (result.deleted) {
                $scope.DeleteSuccess = true;
                window.location.href = "/Project/Task/" + $scope.Task.ProjectId;
            }
        });
    }
	
	$scope.QueryCase = function () {
		$scope.TaskQueryCase.ProjectId = $scope.Task.ProjectId;
		$scope.TaskQueryCase.TaskId = $scope.Task.TaskId;
		
		if ($scope.Task.TaskType == 2 ){
			$scope.TaskQueryCase.CaseType = 1;
		}
		if ($scope.Task.TaskType == 3){
			$scope.TaskQueryCase.CaseType = 2;
		}
        $http.post('/Case/TaskQueryCase', $scope.TaskQueryCase ).success(function (result) {
            $scope.TaskQueryCaseList = result.caselist;
        });

    }
	
	$scope.CheckAll = function (val) {
		val = !val
		if (val==true)
		{
			for (var i=0;i<$scope.TaskQueryCaseList.length;i++) {
				$scope.TaskQueryCaseList[i].IsChecked = true;
			}
		}
		else
		{
			for (var i=0;i<$scope.TaskQueryCaseList.length;i++) {	
				$scope.TaskQueryCaseList[i].IsChecked = false;
			}	
		}

    }	
	
	$scope.ExecutePass = function (val) {
        $http.post('/Case/Execute', {'CaseId': val.CaseId, 'TaskId': val.TaskId, WaveId: val.WaveId, 'Result':val.Result, 'TestData':'', 'Attachment':'', 'BackupInfo':''} ).success(function (result) {
            if (result.executed) {
				val.TestData='';
				val.Attachment='';
				val.BackupInfo='';
            }
        });
    }

    $scope.CantExecutePass = function (val) {
        $http.post('/Case/Execute', {'CaseId': val.CaseId, 'TaskId': val.TaskId, WaveId: val.WaveId, 'Result':val.Result, 'TestData':val.TestData, 'Attachment':val.Attachment, 'BackupInfo':val.BackupInfo} ).success(function (result) {
            if (result.executed) {
				val.NotExecutePass = false;
				val.TestData='';
				val.Attachment='';
				val.BackupInfo='';
            }
        });
    }
	
	$scope.CreateIssue = function (val) {
		$scope.Issue = {ProjectId: 0, Subject:'', Priority: 2, AssignTo: 0,Description:'',CategoryId:1 , IssueId:'',CaseId:'' };
		if (val.IsNeedCreateBug)
		{
            $scope.Issue.CaseId = val.CaseId;
			$scope.Issue.ProjectId = $scope.Task.ProjectId;
			$scope.Issue.Subject = val.Subject;
			$scope.Issue.AssignTo = $scope.UserId;
			$scope.Issue.Description='Test Step:'+val.TestSteps+'<br>'
									+'Expected Result:'+val.ExpectedResult+'<br>'
									+'Test Data:'+val.TestData+'<br>'
									+'Actual Result:'+val.BackupInfo;

			$http.post('/Issue/CreateNewAndLink', $scope.Issue).success(function (result) {
				if (result.created) {
					window.location.href = "/Task/Detail/"+ $scope.Task.ProjectId + "_" + $scope.Task.TaskId;
				}
			});
		}
    }

		
	$scope.RunScript = function(WaveId, Case){
		var CaseId = Case.CaseId;
		$http.post('/RunCase',  { WaveId: WaveId, CaseId: CaseId, UserId: $scope.UserId } ).success(function (result) {
			$scope.RunInfo.isPass = result.isPass;
			$scope.RunInfo.lastStepId = result.lastStepId;
			$scope.RunInfo.retCode = result.retCode;
			$scope.RunInfo.retMsg = result.retMsg;
			$scope.isExecuted = true;

			if ($scope.isExecuted){
				if ($scope.RunInfo.isPass){
					Case.Result=1;
					Case.NotExecutePass=false;
					Case.IsExecuteSucc=true;
					Case.IsExecuteFail=false;
					Case.IsCantExecute=false;
					Case.TestData='';
					Case.Attachment='';
					Case.BackupInfo='';
					Case.WaveId=WaveId;
					$scope.ExecutePass(Case);
				}
				else{
					Case.Result=2;
					Case.NotExecutePass=true;
					Case.IsExecuteSucc=false;
					Case.IsExecuteFail=true;
					Case.IsCantExecute=false;
					Case.TestData='';
					Case.Attachment='';
					Case.BackupInfo='';
					Case.WaveId=WaveId;
					$scope.CantExecutePass(Case);
					
				}
			}
		});
	}

	$scope.RunScriptNew = function(Case){
		var WaveId = new Date().getTime();
		var CaseId = Case.CaseId;
		$http.post('/RunCase',  { WaveId: WaveId, CaseId: CaseId, UserId: $scope.UserId } ).success(function (result) {
			$scope.RunInfo.isPass = result.isPass;
			$scope.RunInfo.lastStepId = result.lastStepId;
			$scope.RunInfo.retCode = result.retCode;
			$scope.RunInfo.retMsg = result.retMsg;
			$scope.isExecuted = true;

			if ($scope.isExecuted){
				if ($scope.RunInfo.isPass){
					Case.Result=1;
					Case.NotExecutePass=false;
					Case.IsExecuteSucc=true;
					Case.IsExecuteFail=false;
					Case.IsCantExecute=false;
					Case.TestData='';
					Case.Attachment='';
					Case.BackupInfo='';
					Case.WaveId=WaveId;
					$scope.ExecutePass(Case);
				}
				else{
					Case.Result=2;
					Case.NotExecutePass=true;
					Case.IsExecuteSucc=false;
					Case.IsExecuteFail=true;
					Case.IsCantExecute=false;
					Case.TestData='';
					Case.Attachment='';
					Case.BackupInfo='';
					Case.WaveId=WaveId;
					$scope.CantExecutePass(Case);
					
				}
			}
		});
	}	
	
	$scope.RunAllScript = function(){
		$scope.CurrWaveId = ''
		$scope.CurrWaveId = new Date().getTime();
		for (var i=0;i<$scope.TaskQueryCaseList.length;i++) {
			if($scope.TaskQueryCaseList[i].IsChecked){
				$scope.RunScript($scope.CurrWaveId, $scope.TaskQueryCaseList[i]);
			}
		}
	}
	
	$scope.GetLatestWaveHistory = function(){
		$scope.LatestWaveId = '';
		$scope.RetWaveInfo = {};
		$http.post('/RunCase/GetLatestWaveHistory',  {} ).success(function (result) {
			$scope.LatestWaveId = result.latest_wave_id;
			$scope.RetWaveInfo = result.ret_wave_info;
		});	
	}
}

function TeamCtrl($scope, $http) {
    $scope.AddSuccess = false;
    $scope.RemoveSuccess = false;
    $scope.MemberCandidate = [];
    $scope.MemberList = [];
    $scope.GetMemberCandidate = function () {
        $http.post('/Team/GetMemberCandidate', { 'ProjectId': $scope.ProjectId }).success(function (result) {
            $scope.MemberCandidate = result.data;
        });
    }
    $scope.GetMemberInProject = function () {
        $http.post('/Team/GetMemberInProject', { 'ProjectId': $scope.ProjectId }).success(function (result) {
            $scope.MemberList = result.data;
        });
    }
    $scope.AddMember = function (email) {
        $scope.AddSuccess = false;
        $scope.RemoveSuccess = false;
        $http.post('/Team/AddMember', { 'ProjectId': $scope.ProjectId, 'Email': email }).success(function (result) {
            if (result.created) {
                $scope.AddSuccess = true;
                $scope.GetMemberCandidate();
                $scope.GetMemberInProject();
            }
        });
    }
    $scope.RemoveMember = function (userId) {
        $scope.AddSuccess = false;
        $scope.RemoveSuccess = false;
        $http.post('/Team/RemoveMember', { 'ProjectId': $scope.ProjectId, 'UserId': userId }).success(function (result) {
            if (result.removed) {
                $scope.RemoveSuccess = true;
                $scope.GetMemberCandidate();
                $scope.GetMemberInProject();
            }
        });
    }
}

function IssueCtrl($scope, $http) {
    $scope.IssueList = [];
    $scope.Query = { PageNo: 1, ProjectId: -1, Subject: '', AssignTo: 0, CategoryId: -1, Open: true, Fixed: true, Closed: false, Canceled: false, RowCount: 0, PageCount: 0 };

	$scope.queryInit = function () {
        $http.post('/Issue/Query', $scope.Query ).success(function (result) {
            $scope.IssueList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }

	$scope.queryIssue = function () {
        $http.post('/Issue/Query', $scope.Query ).success(function (result) {
            $scope.IssueList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
}

function IssueCreateCtrl($scope, $http) {
    $scope.AddSuccess = false;
    editor = UE.getEditor('editor');
    $scope.Issue = { Subject: null, AssignTo: -1, Priority: 2, Description: null, CategoryId: 1 };
    $scope.create = function () {
        $scope.Issue.Description = editor.getContent();
        $http.post('/Issue/CreateNew', $scope.Issue).success(function (result) {
            if (result.created) {
                $scope.AddSuccess = true;
                window.location.href = "/Project/Issue/" + result.ProjectId;
            }
        });
    }
		
}

function IssueUpdateCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
    $scope.ShowUpdate = false;
	$scope.WriteNote = false
	$scope.CommentList = [];
	$scope.CommentQuery = { PageNo: 1,  RowCount: 0, PageCount: 0, CommentType: 1, ObjectId: 0 };
	
    $scope.edit = function () {
        $scope.ShowUpdate = !$scope.ShowUpdate;
        editor = UE.getEditor('editor');
		editor.ready(function(){    
		editor.setContent($scope.Issue.Description);
		})
    }
    $scope.update = function () {

        $scope.Issue.Description = UE.getEditor('editor').getContent();
        $http.post('/Issue/Update', $scope.Issue).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
				window.location.href = "/Issue/Detail/"+ $scope.Issue.ProjectId + "_" + $scope.Issue.IssueId;
            }
        });
    }

    $scope.Delete = function () {
        $http.post('/Issue/Delete', { 'IssueId': $scope.Issue.IssueId }).success(function (result) {
            if (result.deleted) {
                $scope.DeleteSuccess = true;
				window.location.href = "/Project/Issue/" + $scope.Issue.ProjectId;
            }
        });
    }

    $scope.QueryComment = function () {
		$scope.CommentQuery.ObjectId = $scope.Issue.IssueId;
        $http.post('/Comment/Query', $scope.CommentQuery ).success(function (result) {
			$scope.CommentList = result.commentList;
            $scope.CommentQuery.RowCount = result.row_count;
            $scope.CommentQuery.PageCount = result.page_count;
            $scope.CommentQuery.PageNo = result.page_no;
        });
    }
	
    $scope.SubmitComment = function () {
        $http.post('/Comment/Create', { 'CommentType': '1', 'ObjectId': $scope.Issue.IssueId, 'Content': $scope.NoteContent } ).success(function (result) {
			if (result.createcomment) {
				$scope.WriteNote = !$scope.WriteNote;
				window.location.href = "/Issue/Detail/" + $scope.Issue.ProjectId +"_"+$scope.Issue.IssueId;
            }
        });
    }
}

function CaseCtrl($scope, $http) {
	
    $scope.CaseList = [];
    $scope.Query = { PageNo: 1, ProjectId: -1, CaseType: 0, Subject:'', RowCount: 0, PageCount: 0 };
	$scope.queryInit = function () {
        $http.post('/Case/Query', $scope.Query).success(function (result) {
            $scope.CaseList = result.caselist;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
	
    $scope.queryCase = function () {
        $http.post('/Case/Query', $scope.Query).success(function (result) {
            $scope.CaseList = result.caselist;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
	
}

function CaseCreateCtrl($scope, $http) {
	$scope.CaseFieldList = [];
	$scope.CaseInfo = { ProjectId: 0, CaseType: 0, Subject: '', Precondition: '', TestSteps:'', ExpectedResult: '', CaseFieldList: [], AutoRunScriptFile:'' }
	editor1 = UE.getEditor('Precondition');
	editor2 = UE.getEditor('TestSteps');
	editor3 = UE.getEditor('ExpectedResult');
    $scope.query = function () {	
			$scope.CaseFieldList = [];
			$http.post('/CaseField/Query', { ProjectId: $scope.CaseInfo.ProjectId } ).success(function (result) {
			$scope.CaseFieldList = result.casefieldslist;
        });
    }

    $scope.create = function () {
		$scope.CaseInfo.Precondition = editor1.getContent();
		$scope.CaseInfo.TestSteps = editor2.getContent();
		$scope.CaseInfo.ExpectedResult = editor3.getContent();	
		$scope.CaseInfo.CaseFieldList = $scope.CaseFieldList;
        $http.post('/Case/CreateNew', $scope.CaseInfo).success(function (result) {
			window.location.href = "/Project/Case/" + $scope.CaseInfo.ProjectId;
        });
    }
}

function CaseUpdateCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.DeleteSuccess = false;
    $scope.ShowUpdate = false;
	$scope.WriteNote = false;
	
	$scope.NotExecutePass = false;
	$scope.IsExecuteSucc = false;
	$scope.IsExecuteFail = false;
	$scope.IsCantExecute = false;
	$scope.IsNeedCreateBug = false;
	
	$scope.CaseSettingList = [];
	$scope.CommentList = [];
	$scope.CommentQuery = { PageNo: 1,  RowCount: 0, PageCount: 0, CommentType: 2, ObjectId: 0 };
	$scope.CustomFieldsComp = { FieldValueSelected: '', CustomFieldValue:'' }
	$scope.ChangeHistoryQuery = { PageNo: 1,  RowCount: 0, PageCount: 0, CaseId: ''};
	$scope.ChangeHistoryList = [];	
	$scope.ExecuteHistoryQuery = { PageNo: 1,  RowCount: 0, PageCount: 0, CaseId: ''};
	$scope.ExecuteHistoryList = [];
	$scope.ExecuteCaseQuery  = { CaseId: '', TaskId: 0, WaveId:'', Result: 0, TestData:'', Attachment:'', BackupInfo:'' };
	$scope.LinkBugList = [];
	$scope.Issue = { Subject:'', AssignTo: -1, Priority: 2, Description: '', CategoryId: 1, IssueId: 0 };
	
	$scope.RunInfo = {};
	$scope.WaveId = null;
	$scope.UserId = 0;	
	$scope.AutoRunHistoryQuery = { PageNo: 1,  RowCount: 0, PageCount: 0, CaseId: ''};
	$scope.AutoRunHistoryList = [];		  
		
    $scope.GetExistingFields = function () {
        $http.post('/Case/GetExistingFields', $scope.Case).success(function (result) {
		$scope.CaseSettingList = result.CaseSettingList;
        });
    }	
	
    $scope.edit = function () {
        $scope.ShowUpdate = !$scope.ShowUpdate;
        editor1 = UE.getEditor('editorPreCondition');
		editor2 = UE.getEditor('editorTestSteps');
		editor3 = UE.getEditor('editorExpectedResult');
		editor1.ready(function(){
			editor1.setContent($scope.Case.PreCondition);
		})
		editor2.ready(function(){
			editor2.setContent($scope.Case.TestSteps);
		})
		editor3.ready(function(){
			editor3.setContent($scope.Case.ExpectedResult);
		})
		if (window.frames['calliframe1'].document.body)
		{
			window.frames['calliframe1'].document.body.innerHTML=$scope.Case.AutoRunScriptFile;
		}			
    }
    $scope.update = function () {
        $scope.Case.PreCondition = UE.getEditor('editorPreCondition').getContent();
        $scope.Case.TestSteps = UE.getEditor('editorTestSteps').getContent();
        $scope.Case.ExpectedResult = UE.getEditor('editorExpectedResult').getContent();
		if (window.frames['calliframe1'].document.body)
		{
			$scope.Case.AutoRunScriptFile = window.frames['calliframe1'].document.body.innerHTML;
		}		
        $http.post('/Case/Update', $scope.Case).success(function (result) {
            if (result.updated) {
                $scope.UpdateSuccess = true;
				window.location.href = "/Case/Detail/" + $scope.Case.ProjectId + "_" + $scope.Case.CaseId;
            }
        });
    }

    $scope.Delete = function () {
        $http.post('/Case/Delete', { 'CaseId': $scope.Case.CaseId }).success(function (result) {
            if (result.deleted) {
                $scope.DeleteSuccess = true;
				window.location.href = "/Project/Case/" + $scope.Case.ProjectId;
            }
        });
    }
	
    $scope.ExecutePass = function () {
		$scope.ExecuteCaseQuery.CaseId = $scope.Case.CaseId;
        $http.post('/Case/Execute', $scope.ExecuteCaseQuery ).success(function (result) {
            if (result.executed) {
				$scope.ExecuteCaseQuery.TestData='';
				$scope.ExecuteCaseQuery.Attachment='';
				$scope.ExecuteCaseQuery.BackupInfo='';
				window.location.href = "/Case/Detail/" + $scope.Case.ProjectId + "_" + $scope.Case.CaseId;
            }
        });
    }
	
    $scope.CantExecutePass = function () {
		$scope.ExecuteCaseQuery.CaseId = $scope.Case.CaseId;
		if (window.frames['calliframe'].document.body)
		{
			$scope.ExecuteCaseQuery.Attachment = window.frames['calliframe'].document.body.innerHTML;
		}
		
        $http.post('/Case/Execute', $scope.ExecuteCaseQuery ).success(function (result) {
            if (result.executed) {
				if (window.frames['calliframe'].document.body)
				{
					window.frames['calliframe'].document.body.innerHTML='';
				}
				document.getElementById('frm_attachment').reset();
				$scope.NotExecutePass = false;
				$scope.ExecuteCaseQuery.TestData='';
				$scope.ExecuteCaseQuery.Attachment='';
				$scope.ExecuteCaseQuery.BackupInfo='';
				window.location.href = "/Case/Detail/" + $scope.Case.ProjectId + "_" + $scope.Case.CaseId;

            }
        });
    }
	
    $scope.CantExecutePassBack = function () {
		if (window.frames['calliframe'].document.body)
		{
			window.frames['calliframe'].document.body.innerHTML='';
		}
		document.getElementById('frm_attachment').reset();
		$scope.NotExecutePass = false;
		$scope.ExecuteCaseQuery.TestData='';
		$scope.ExecuteCaseQuery.Attachment='';
		$scope.ExecuteCaseQuery.BackupInfo='';
    }
	
    $scope.QueryComment = function () {
		$scope.CommentQuery.ObjectId = $scope.Case.CaseId;
        $http.post('/Comment/Query', $scope.CommentQuery ).success(function (result) {
			$scope.CommentList = result.commentList;
            $scope.CommentQuery.RowCount = result.row_count;
            $scope.CommentQuery.PageCount = result.page_count;
            $scope.CommentQuery.PageNo = result.page_no;
        });
    }
	
    $scope.SubmitComment = function () {
        $http.post('/Comment/Create', { 'CommentType': '2', 'ObjectId': $scope.Case.CaseId, 'Content': $scope.NoteContent } ).success(function (result) {
			if (result.createcomment) {
				$scope.WriteNote = !$scope.WriteNote;
				window.location.href = "/Case/Detail/"+ $scope.Query.ProjectId + "_" + $scope.Case.CaseId;
            }
        });
    }

	$scope.GetChangeHistory = function () {
		$scope.ChangeHistoryQuery.CaseId = $scope.Case.CaseId;
        $http.post('/Case/ChangeHistory', $scope.ChangeHistoryQuery ).success(function (result) {
			$scope.ChangeHistoryList = result.change_history_list;
            $scope.ChangeHistoryQuery.RowCount = result.row_count;
            $scope.ChangeHistoryQuery.PageCount = result.page_count;
            $scope.ChangeHistoryQuery.PageNo = result.page_no;
        });
    }

    $scope.GetExecuteHistory = function () {
		$scope.ExecuteHistoryQuery.CaseId = $scope.Case.CaseId;
        $http.post('/Case/ExecuteHistory', $scope.ExecuteHistoryQuery ).success(function (result) {
			$scope.ExecuteHistoryList = result.execute_history_list;
            $scope.ExecuteHistoryQuery.RowCount = result.row_count;
            $scope.ExecuteHistoryQuery.PageCount = result.page_count;
            $scope.ExecuteHistoryQuery.PageNo = result.page_no;
        });
    }

    $scope.GetCaseLinkBug = function () {
        $http.post('/Case/GetLinkBug', {CaseId: $scope.Case.CaseId} ).success(function (result) {
			$scope.LinkBugList = result.retLinkBugList;
        });
    }
	
	$scope.CheckBoxSelect = function () {
		if (document.getElementById('needCreateBug').checked)
		{

			$scope.IsNeedCreateBug = true;
		}
		else
		{
			$scope.IsNeedCreateBug = false;
		}
    }
	
	$scope.CreateIssue = function () {
		if ($scope.IsNeedCreateBug)
		{
            $scope.Issue.CaseId = $scope.Case.CaseId;
			$scope.Issue.Subject = $scope.Case.Subject;
			$scope.Issue.ProjectId = $scope.Case.ProjectId;
			$scope.Issue.Description='Test Step:'+$scope.Case.TestSteps+'<br>'
									+'Expected Result:'+$scope.Case.ExpectedResult+'<br>'
									+'Test Data:'+$scope.ExecuteCaseQuery.TestData+'<br>'
									+'Actual Result:'+$scope.ExecuteCaseQuery.BackupInfo;
									
			if (window.frames['calliframe'].document.body)
			{
				$scope.Issue.Description= $scope.Issue.Description
										+  'Link:<a href="'+ window.frames['calliframe'].document.body.innerHTML+ '">'
										+  window.frames['calliframe'].document.body.innerHTML + '</a>';
			}

			$http.post('/Issue/CreateNewAndLink', $scope.Issue).success(function (result) {
				if (result.created) {
                    window.location.href = "/Case/Detail/" + $scope.Case.ProjectId + "_" + $scope.Case.CaseId;
				}
			});
		}
		
    }

	
	$scope.RunScript = function(){
		$scope.WaveId = new Date().getTime(); 
		$http.post('/RunCase',  { WaveId: $scope.WaveId, CaseId: $scope.Case.CaseId, UserId: $scope.UserId } ).success(function (result) {
			$scope.RunInfo.isPass = result.isPass;
			$scope.RunInfo.lastStepId = result.lastStepId;
			$scope.RunInfo.retCode = result.retCode;
			$scope.RunInfo.retMsg = result.retMsg;
			window.location.href = "/Case/Detail/" + $scope.Case.ProjectId + "_" + $scope.Case.CaseId;
		});
	}
	
	$scope.GetAutorunHistory = function () {
		$scope.AutoRunHistoryQuery.CaseId = $scope.Case.CaseId;
		$http.post('/RunCase/GetOneCaseHistory', $scope.AutoRunHistoryQuery ).success(function (result) {
			$scope.AutoRunHistoryList = result.wave_info_all;
			$scope.AutoRunHistoryQuery.RowCount = result.row_count;
			$scope.AutoRunHistoryQuery.PageCount = result.page_count;
			$scope.AutoRunHistoryQuery.PageNo = result.page_no;
		});
	}

}

function ScriptCtrl($scope, $http, cfpLoadingBar) {
	$scope.CaseId = '';
	$scope.StepList = [];

	$scope.Query_String = {CaseId: '', Query_String:''};
	$scope.QuerySucc = false;
	$scope.QueryRet = {Id: 0, StepId: 0, OperType: 0, ParameterName: '', ParameterValue:''};
	
	$scope.OperType = {ValReplace: 1, ValBind: 2, InsertFun: 3};
	$scope.ParemeterTypeNew = {StringVal: 1, RandVal: 2, TimeStamp: 3};
	$scope.ReplaceWay = {All:1,  CurrItem:2};
	$scope.ParamBindQuery = {FieldId: 0, ScriptId: 0, StepId: 0, CaseId: '', OperType: $scope.OperType.ValReplace, ParameterName:'', ParameterValue: '',ParemeterTypeNew: $scope.ParemeterTypeNew.StringVal, ParameterNameNew:'',ParameterValueNew:'', ReplaceWay: $scope.ReplaceWay.All, IsParent:1,  BindStepId: 0, LefeStr:'',RightStr:'' };
	$scope.currfield = {};
	$scope.bindstep = {};
	$scope.IsAddParamSucc = 0;	

    $scope.start = function() {
      cfpLoadingBar.start();
    };

    $scope.complete = function () {
      cfpLoadingBar.complete();
    }
	
	$scope.Query = function () {
		$scope.start();
		$http.post('/Case/Script/Query', { CaseId: $scope.CaseId } ).success(function (result) {
			$scope.StepList = result.steplist;
			$scope.complete();
      });
    }

	$scope.QueryRetData = function (step) {
		if (step.RetData.length==0 || step.RetDataShow==false){
			$http.post('/Case/Script/QueryScriptRetData', { CaseId: $scope.CaseId, StepId: step.StepId } ).success(function (result) {
				if (result.retdatashow) {
					step.RetDataShow = result.retdatashow;
					step.RetData = result.retdata;
				}
			});	
		}
    }
	
	$scope.QueryBindParamRetData = function(currfield) {
		$scope.start();
		var stepid = currfield.QueryRet.StepId;
		$scope.bindstep = {};
		for(var stepkey in $scope.StepList){
			var step = $scope.StepList[stepkey];
			if (stepid==step.StepId){
				$scope.bindstep = step;
				break;
			}
		}
		$scope.QueryRetData($scope.bindstep);
		$scope.complete();
	}
   	
	$scope.QueryString= function () {
		$scope.Query_String.CaseId = $scope.CaseId;
		$http.post('/Case/Script/QueryString',  $scope.Query_String ).success(function (result) {
			$scope.QuerySucc = result.querysucc;
			$scope.QueryRet = result.queryret;
        });
    }
	
	$scope.QueryStringNew= function (field) {
		$http.post('/Case/Script/QueryString',  {CaseId: $scope.CaseId, Query_String:field.ParameterValue} ).success(function (result) {
			field.QueryRet = result.queryret;
		});
    }	
	
	$scope.doParamInit = function(step, field){
		 $scope.currfield  = {};
		 $scope.ParamBindQuery = {FieldId: 0, ScriptId: 0, StepId: 0, CaseId: '', OperType: $scope.OperType.ValReplace, ParameterName:'', ParameterValue: '',ParemeterTypeNew: $scope.ParemeterTypeNew.StringVal, ParameterNameNew:'',ParameterValueNew:'', ReplaceWay: $scope.ReplaceWay.All, IsParent:1,  BindStepId: 0, LefeStr:'',RightStr:'' };
		 $scope.ParamBindQuery.FieldId = field.Id;
		 $scope.ParamBindQuery.ScriptId = step.Id;
		 $scope.ParamBindQuery.StepId = step.StepId;
		 $scope.ParamBindQuery.CaseId = step.CaseId;
		 $scope.ParamBindQuery.OperType = field.QueryRet.OperType;
		 $scope.ParamBindQuery.ParameterName  = field.ParameterName;
		 $scope.ParamBindQuery.ParameterValue  = field.ParameterValue;
		 $scope.ParamBindQuery.ParameterNameNew = field.ParameterName+'_'+ step.StepId+'_'+ field.Id;
		 $scope.ParamBindQuery.ParameterValueNew = field.ParameterValue;
		 $scope.ParamBindQuery.ReplaceWay = $scope.ReplaceWay.All;
		 $scope.ParamBindQuery.IsParent = 1;
		 $scope.ParamBindQuery.BindStepId = field.QueryRet.StepId;
		 $scope.IsAddParamSucc = 0;
		 $scope.currfield = field;
		 $scope.bindstep = step;
		 var $myModal = $('#my-popup');
		 $myModal.modal();
	}
	
	$scope.doParamSubmit = function(){
		$scope.IsAddParamSucc = 0;
		$http.post('/Case/Script/DoParamSubmit',  $scope.ParamBindQuery ).success(function (result) {
		if (result.added) {
			$scope.IsAddParamSucc = 1;
			var $myModal = $('#my-popup');
			$myModal.modal('close');
		}
		else{
			$scope.IsAddParamSucc = 2;
			
		}
      });
	}

	$scope.CancelParam = function(field){
		$scope.IsAddParamSucc = 0;
		$http.post('/Case/Script/CancelParam',  {FieldId: field.Id} ).success(function (result) {
			if (result.canceled) {
				field.IsParamBind = false;
				field.ParamBind = {};
			}
		});
	}
	
	$scope.RunInfo = {};
	$scope.WaveId = '';
	$scope.UserId = 0;
	$scope.isExecuted = false;
	$scope.WaveInfo = [];
	$scope.RunScript = function(){
		$scope.WaveId = new Date().getTime(); 
		$http.post('/RunCase',  { WaveId: $scope.WaveId, CaseId: $scope.CaseId, UserId: $scope.UserId } ).success(function (result) {
			$scope.RunInfo.isPass = result.isPass;
			$scope.RunInfo.lastStepId = result.lastStepId;
			$scope.RunInfo.retCode = result.retCode;
			$scope.RunInfo.retMsg = result.retMsg;
			$scope.isExecuted = true;
			$scope.GetExecuteHistoryWaveInfo($scope.WaveId);
		});
	}
	
	$scope.GetExecuteHistoryWaveInfo = function(waveid){
		$http.post('/RunCase/GetHistoryByWaveIdAndCaseId',  { WaveId: waveid, CaseId: $scope.CaseId } ).success(function (result) {
			$scope.WaveInfo = result.wave_info;
		});	
	}
}

function UpdateProfileCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.Error = false;
    $scope.update = function () {
        $scope.UpdateSuccess = false;
        $scope.Error = false;
        $http.post('/UpdateProfile', $scope.User).success(function (result) {
            if (result.Updated) {
                $scope.UpdateSuccess = true;
                $scope.Error = false;
            }
            else {
                $scope.UpdateSuccess = false;
                $scope.Error = true;
            }
        });
    }
}

function ChangePasswordCtrl($scope, $http) {
    $scope.UpdateSuccess = false;
    $scope.Error = false;
    $scope.update = function () {
        $scope.UpdateSuccess = false;
        $scope.Error = false;
        $http.post('/ChangePassword', $scope.User).success(function (result) {
            if (result.Updated) {
                $scope.UpdateSuccess = true;
                $scope.Error = false;
            }
            else {
                $scope.UpdateSuccess = false;
                $scope.Error = true;
            }
        });
    }
}

function UserManagementCtrl($scope, $http) {
    $scope.Success = false;
    $scope.UserList = [];
    $scope.Query = { PageNo: 1, Word: '', Status: -1, RowCount: 0, PageCount: 0 };
    $scope.query = function () {
        $http.post('/QueryUser', $scope.Query).success(function (result) {
            $scope.UserList = result.data;
            $scope.Query.RowCount = result.row_count;
            $scope.Query.PageCount = result.page_count;
            $scope.Query.PageNo = result.page_no;
        });
    }
    $scope.enable = function (userid) {
        $scope.Success = false;
        $http.post('/EnableUser', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.disable = function (userid) {
        $scope.Success = false;
        $http.post('/DisableUser', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.resetpass = function (userid) {
        $scope.Success = false;
        $http.post('/ResetPassword', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.assignadmin = function (userid) {
        $scope.Success = false;
        $http.post('/AssignAdmin', { UserId: userid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
}

function CustomFieldCtrl($scope, $http) {
    $scope.Success = false;
    $scope.Exist = false;
		$scope.MyNewField={'CustomFieldDesc':''}
		$scope.MyNewFieldValue={'FieldValue':''}
		$scope.Query={ProjectId:-1}
	    
		$scope.retBugList = [];
		$scope.retCaseList = [];
		$scope.retTaskList = [];
	
    $scope.query = function () {
        $http.post('/Setting/QueryCustomField', $scope.Query).success(function (result) {
            $scope.retBugList = result.retBugList;
			$scope.retCaseList = result.retCaseList;
			$scope.retTaskList = result.retTaskList;
        });
    }
    $scope.enableField = function (customfieldid) {
        $scope.Success = false;
        $http.post('/Setting/EnableCustomField', { CustomFieldId: customfieldid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.disableField = function (customfieldid) {
        $scope.Success = false;
        $http.post('/Setting/DisableCustomField', { CustomFieldId: customfieldid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.delField = function (customfieldid) {
        $scope.Success = false;
        $http.post('/Setting/DeleteCustomField', { CustomFieldId: customfieldid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.saveFieldDesc = function (customfieldid) {
        $scope.Success = false;
        $http.post('/Setting/SaveCustomFieldDesc', { CustomFieldId: customfieldid, CustomFieldDesc: $scope.MyNewField.CustomFieldDesc }).success(function () {
			$scope.Success = true;
            $scope.query();
			$scope.bugCustomField.CustomFieldDesc=$scope.MyNewField.CustomFieldDesc
        });
    }
	
    $scope.createField = function () {
        $scope.Success = false;
        $scope.Exist = false;
        $http.post('/Setting/CreateCustomField', { ProjectId: $scope.Query.ProjectId, CustomField: $scope.NewCustomField, ObjectType: $scope.NewObjectType }).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
			$scope.NewCustomField = ""
			$scope.NewObjectType = ""
            $scope.query();
        });
    }
	
    $scope.enableFieldValue = function (fieldvalueid) {
        $scope.Success = false;
        $http.post('/Setting/EnableFieldValue', { FieldValueId: fieldvalueid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.disableFieldValue = function (fieldvalueid) {
        $scope.Success = false;
        $http.post('/Setting/DisableFieldValue', { FieldValueId: fieldvalueid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
    $scope.delFieldValue = function (fieldvalueid) {
        $scope.Success = false;
        $http.post('/Setting/DeleteFieldValue', { FieldValueId: fieldvalueid }).success(function () {
            $scope.Success = true;
            $scope.query();
        });
    }
	
    $scope.saveFieldValue = function (fieldvalueid) {
        $scope.Success = false;
        $http.post('/Setting/SaveFieldValue', { FieldValueId: fieldvalueid, FieldValue: $scope.MyNewFieldValue.FieldValue }).success(function () {
			$scope.Success = true;
            $scope.query();
			$scope.fieldvalue.FieldValue=$scope.MyNewFieldValue.FieldValue
        });
    }
	
    $scope.createFieldValue = function () {
        $scope.Success = false;
        $scope.Exist = false;
        $http.post('/Setting/CreateFieldValue', { ProjectId: $scope.Query.ProjectId, CustomFieldId: $scope.SelectedFieldValue.CustomFieldId, FieldValue: $scope.NewFieldValue }).success(function (result) {
            if (result.status) {
                $scope.Success = false;
                $scope.Exist = true;
            } else {
                $scope.Success = true;
                $scope.Exist = false;
            }
            $scope.query();
			$scope.SelectedFieldValue = ""
			$scope.NewFieldValue = ""
        });
    }
}

function UploadCtrl($scope, $upload) {
	$scope.onFileSelect = function($files) {
		for (var i = 0; i < $files.length; i++) {      
			var file = $files[i];
			$scope.upload = $upload.upload({
				url: '/uploadfile', 
				data: {myObj: $scope.myModelObj},
				file: file, 
		  }).progress(function(evt) {        
				console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
		  }).success(function(data, status, headers, config) {
				console.log(data);
		  });

		} 
    };
}


function MonCtrl($scope, $http){
	$scope.cpuInfo = []
	$scope.memInfo = []
	$scope.Query={GetData:1}
	
    $scope.getData = function () {
		$scope.cpuInfo = []
		$scope.memInfo = []
        $http.post('/Monitor/GetData', $scope.Query).success(function (result) {
            $scope.cpuInfo = result.cpuInfo;
			$scope.memInfo = result.memInfo;
        });
    }
}

angular.bootstrap(document, ['TestSys']);