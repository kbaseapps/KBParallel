
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: TaskResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "function",
    "params",
    "returned",
    "error",
    "run_context"
})
public class TaskResult {

    /**
     * <p>Original spec-file type: Function</p>
     * 
     * 
     */
    @JsonProperty("function")
    private Function function;
    @JsonProperty("params")
    private UObject params;
    @JsonProperty("returned")
    private UObject returned;
    @JsonProperty("error")
    private UObject error;
    /**
     * <p>Original spec-file type: RunContext</p>
     * <pre>
     * location = local | njsw
     * job_id = '' | [njsw_job_id]
     * May want to add: AWE node ID, client group, total run time, etc
     * </pre>
     * 
     */
    @JsonProperty("run_context")
    private RunContext runContext;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Function</p>
     * 
     * 
     */
    @JsonProperty("function")
    public Function getFunction() {
        return function;
    }

    /**
     * <p>Original spec-file type: Function</p>
     * 
     * 
     */
    @JsonProperty("function")
    public void setFunction(Function function) {
        this.function = function;
    }

    public TaskResult withFunction(Function function) {
        this.function = function;
        return this;
    }

    @JsonProperty("params")
    public UObject getParams() {
        return params;
    }

    @JsonProperty("params")
    public void setParams(UObject params) {
        this.params = params;
    }

    public TaskResult withParams(UObject params) {
        this.params = params;
        return this;
    }

    @JsonProperty("returned")
    public UObject getReturned() {
        return returned;
    }

    @JsonProperty("returned")
    public void setReturned(UObject returned) {
        this.returned = returned;
    }

    public TaskResult withReturned(UObject returned) {
        this.returned = returned;
        return this;
    }

    @JsonProperty("error")
    public UObject getError() {
        return error;
    }

    @JsonProperty("error")
    public void setError(UObject error) {
        this.error = error;
    }

    public TaskResult withError(UObject error) {
        this.error = error;
        return this;
    }

    /**
     * <p>Original spec-file type: RunContext</p>
     * <pre>
     * location = local | njsw
     * job_id = '' | [njsw_job_id]
     * May want to add: AWE node ID, client group, total run time, etc
     * </pre>
     * 
     */
    @JsonProperty("run_context")
    public RunContext getRunContext() {
        return runContext;
    }

    /**
     * <p>Original spec-file type: RunContext</p>
     * <pre>
     * location = local | njsw
     * job_id = '' | [njsw_job_id]
     * May want to add: AWE node ID, client group, total run time, etc
     * </pre>
     * 
     */
    @JsonProperty("run_context")
    public void setRunContext(RunContext runContext) {
        this.runContext = runContext;
    }

    public TaskResult withRunContext(RunContext runContext) {
        this.runContext = runContext;
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
        return ((((((((((((("TaskResult"+" [function=")+ function)+", params=")+ params)+", returned=")+ returned)+", error=")+ error)+", runContext=")+ runContext)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
