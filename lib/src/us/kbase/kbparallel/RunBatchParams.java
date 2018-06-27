
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: RunBatchParams</p>
 * <pre>
 * * Run a set of multiple batch jobs, either locally or remotely. If run remotely, they will be
 * * started using NarrativeJobService#run_job. If run locally, the job will be started using the
 * * callback server.
 * *
 * * Required arguments:
 * *   tasks - a list of task objects to be run in batch (see the Task type).
 * * Optional arguments:
 * *   runner - one of 'local_serial', 'local_parallel', or 'parallel':
 * *      local_serial - run tasks on the node in serial, ignoring the concurrent task limits
 * *      local_parallel - run multiple tasks on the node in parallel. Unless you know where your
 * *        job will run, you probably don't want to set this higher than 2
 * *      parallel - look at both the local task and njsw task limits and operate appropriately.
 * *        Therefore, you could always just select this option and tweak the task limits to get
 * *        either serial_local or parallel_local behavior.
 * *   concurrent_njsw_tasks - how many concurrent tasks to run remotely on NJS. This has a
 * *     maximum of 50.
 * *   concurrent_local_tasks - how many concurrent tasks to run locally. This has a hard maximum
 * *     of 20, but you will only want to set this to about 2 due to resource limitations.
 * *   max_retries - how many times to re-attempt failed jobs. This has a minimum of 1 and
 * *     maximum of 5.
 * *   parent_job_id - you can manually pass in a custom job ID which will be assigned to NJS
 * *     sub-jobs that are spawned by KBParallel. This is useful if you need to track the running
 * *     tasks that were started by KBParallel.
 * *   workspace_id - a custom workspace ID to assign to new NJS jobs that are spawned by
 * *     KBParallel.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "tasks",
    "runner",
    "concurrent_local_tasks",
    "concurrent_njsw_tasks",
    "max_retries",
    "parent_job_id",
    "workspace_id"
})
public class RunBatchParams {

    @JsonProperty("tasks")
    private List<Task> tasks;
    @JsonProperty("runner")
    private String runner;
    @JsonProperty("concurrent_local_tasks")
    private Long concurrentLocalTasks;
    @JsonProperty("concurrent_njsw_tasks")
    private Long concurrentNjswTasks;
    @JsonProperty("max_retries")
    private Long maxRetries;
    @JsonProperty("parent_job_id")
    private String parentJobId;
    @JsonProperty("workspace_id")
    private String workspaceId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("tasks")
    public List<Task> getTasks() {
        return tasks;
    }

    @JsonProperty("tasks")
    public void setTasks(List<Task> tasks) {
        this.tasks = tasks;
    }

    public RunBatchParams withTasks(List<Task> tasks) {
        this.tasks = tasks;
        return this;
    }

    @JsonProperty("runner")
    public String getRunner() {
        return runner;
    }

    @JsonProperty("runner")
    public void setRunner(String runner) {
        this.runner = runner;
    }

    public RunBatchParams withRunner(String runner) {
        this.runner = runner;
        return this;
    }

    @JsonProperty("concurrent_local_tasks")
    public Long getConcurrentLocalTasks() {
        return concurrentLocalTasks;
    }

    @JsonProperty("concurrent_local_tasks")
    public void setConcurrentLocalTasks(Long concurrentLocalTasks) {
        this.concurrentLocalTasks = concurrentLocalTasks;
    }

    public RunBatchParams withConcurrentLocalTasks(Long concurrentLocalTasks) {
        this.concurrentLocalTasks = concurrentLocalTasks;
        return this;
    }

    @JsonProperty("concurrent_njsw_tasks")
    public Long getConcurrentNjswTasks() {
        return concurrentNjswTasks;
    }

    @JsonProperty("concurrent_njsw_tasks")
    public void setConcurrentNjswTasks(Long concurrentNjswTasks) {
        this.concurrentNjswTasks = concurrentNjswTasks;
    }

    public RunBatchParams withConcurrentNjswTasks(Long concurrentNjswTasks) {
        this.concurrentNjswTasks = concurrentNjswTasks;
        return this;
    }

    @JsonProperty("max_retries")
    public Long getMaxRetries() {
        return maxRetries;
    }

    @JsonProperty("max_retries")
    public void setMaxRetries(Long maxRetries) {
        this.maxRetries = maxRetries;
    }

    public RunBatchParams withMaxRetries(Long maxRetries) {
        this.maxRetries = maxRetries;
        return this;
    }

    @JsonProperty("parent_job_id")
    public String getParentJobId() {
        return parentJobId;
    }

    @JsonProperty("parent_job_id")
    public void setParentJobId(String parentJobId) {
        this.parentJobId = parentJobId;
    }

    public RunBatchParams withParentJobId(String parentJobId) {
        this.parentJobId = parentJobId;
        return this;
    }

    @JsonProperty("workspace_id")
    public String getWorkspaceId() {
        return workspaceId;
    }

    @JsonProperty("workspace_id")
    public void setWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
    }

    public RunBatchParams withWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((("RunBatchParams"+" [tasks=")+ tasks)+", runner=")+ runner)+", concurrentLocalTasks=")+ concurrentLocalTasks)+", concurrentNjswTasks=")+ concurrentNjswTasks)+", maxRetries=")+ maxRetries)+", parentJobId=")+ parentJobId)+", workspaceId=")+ workspaceId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
