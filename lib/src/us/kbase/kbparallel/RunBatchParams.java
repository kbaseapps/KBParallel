
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
 * runner = serial_local | parallel_local | parallel
 *     serial_local will run tasks on the node in serial, ignoring the concurrent
 *         task limits
 *     parallel_local will run multiple tasks on the node in parallel, and will
 *         ignore the njsw_task parameter. Unless you know where your job will
 *         run, you probably don't want to set this higher than 2
 *     parallel will look at both the local task and njsw task limits and operate
 *         appropriately. Therefore, you could always just select this option and
 *         tweak the task limits to get either serial_local or parallel_local
 *         behavior.
 * TODO:
 * wsid - if defined, the workspace id or name (service will handle either string or
 *        int) on which to attach the job. Anyone with permissions to that WS will
 *        be able to view job status for this run.
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
    "max_retries"
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
        return ((((((((((((("RunBatchParams"+" [tasks=")+ tasks)+", runner=")+ runner)+", concurrentLocalTasks=")+ concurrentLocalTasks)+", concurrentNjswTasks=")+ concurrentNjswTasks)+", maxRetries=")+ maxRetries)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
