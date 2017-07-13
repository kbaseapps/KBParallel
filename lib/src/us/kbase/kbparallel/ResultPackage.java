
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
 * <p>Original spec-file type: ResultPackage</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "function",
    "result",
    "error",
    "run_context"
})
public class ResultPackage {

    /**
     * <p>Original spec-file type: Function</p>
     * <pre>
     * Specifies a specific KBase module function to run
     * </pre>
     * 
     */
    @JsonProperty("function")
    private Function function;
    @JsonProperty("result")
    private UObject result;
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
     * <pre>
     * Specifies a specific KBase module function to run
     * </pre>
     * 
     */
    @JsonProperty("function")
    public Function getFunction() {
        return function;
    }

    /**
     * <p>Original spec-file type: Function</p>
     * <pre>
     * Specifies a specific KBase module function to run
     * </pre>
     * 
     */
    @JsonProperty("function")
    public void setFunction(Function function) {
        this.function = function;
    }

    public ResultPackage withFunction(Function function) {
        this.function = function;
        return this;
    }

    @JsonProperty("result")
    public UObject getResult() {
        return result;
    }

    @JsonProperty("result")
    public void setResult(UObject result) {
        this.result = result;
    }

    public ResultPackage withResult(UObject result) {
        this.result = result;
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

    public ResultPackage withError(UObject error) {
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

    public ResultPackage withRunContext(RunContext runContext) {
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
        return ((((((((((("ResultPackage"+" [function=")+ function)+", result=")+ result)+", error=")+ error)+", runContext=")+ runContext)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
